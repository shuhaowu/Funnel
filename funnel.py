#!/usr/bin/env python

import markdown
import os
import os.path
from datetime import datetime
import re
import json

SECTION_HEADERS_REGEX = re.compile(r"(===)\W*(\w+)\W*(===)")
SECTION_BODIES_REGEX = r"===\W*{name}\W*===(.+)===\W*{name}\W*==="
ACCEPTED_EXTENSIONS = ("markdown", "md", "mkd", "txt")

class NotFound(LookupError): pass

# Dammit Jim, our markdown files looks like HTTP requests.

def parse_meta(meta):
  """Parses through the meta of a markdown file. The structure is:

      key: value
      key: value # comment
      key: value

  This attempts to parse value using eval, upon any sort of error, it will try
  to convert value to an unicode. Example:

      ohai: yay bare words
      list: ["lists", "are", "awesome"]
      op: 1 + 2

  Will become:
      {
        "ohai": "yay bare words"
        "list": ["lists", "are", "awesome"]
        "op": 3
      }
  """
  m = {}
  for i, line in enumerate(meta.strip().split(os.linesep)):
    line = line.strip()

    # Note that in a regular file there will be no empty lines..
    # That is blocked by the fact that we split at the first \n\n.
    if not line or line.startswith("#"): # comment or empty line..
      continue

    line = line.split("#", 1)[0] # comments...
    _temp = line.split(":", 1)
    if len(_temp) != 2:
      raise ValueError("Format of the line is wrong for meta on line {0} with text {1}".format(i, line))
    key = _temp[0].strip()
    value = _temp[1].strip()
    # guess that this is not python code. Because eval will eval things like
    # file to <type 'file'>

    try:
      value = json.loads(value)
    except ValueError:
      value = unicode(value)

    m[key] = value

  return m

def parse_content(content):
  """Parses through the content of a file. Converts using markdown.

  Note that funnel uses sections and sections are defined as:

      === section name ===

      markdown here

      === section name ===

  The two `=== section name ==` are the boundaries. Everything outside of those
  boundaries won't count.

  This method returns a dictionary of section_name: html. If no
  section is defined, the section name of "main" will be used.
  """

  content = content.strip()
  sections = SECTION_HEADERS_REGEX.findall(content)
  sections = {s[1] for s in sections}
  if len(sections) == 0:
    return {"main": markdown.markdown(content)}
  else:
    s = {}
    for section in sections:
      matches = re.findall(SECTION_BODIES_REGEX.format(name=section), content, flags=re.S)
      if not len(matches):
        raise ValueError("Cannot find section {0}. Check for unmatched ending tags?".format(section))
      md = matches[0].strip()
      s[section] = markdown.markdown(md)

    return s

def parse_all(text):
  """Parses through the text of a markdown file.

  Returns meta, content. See parse_meta and parse_content"""

  text = text.strip()

  text = text.split(os.linesep * 2, 1)

  meta = ""
  content = ""

  if len(text) > 0:
    meta = text[0].strip()
    if len(text) > 1:
      content = text[1].strip()


  return parse_meta(meta), parse_content(content)

def get_filename(root, folder, name):
  for ext in ACCEPTED_EXTENSIONS:
    fn = os.path.join(root, folder, name + "." + ext)
    if os.path.exists(fn):
      return fn

  fn = os.path.join(".", folder, name)
  return fn if os.path.exists(fn) else None

def get_config(root):
  if os.path.exists(os.path.join(root, "funnel.config")):
    with open(os.path.join(root, "funnel.config")) as f:
      data = f.read()

    return parse_meta(data)
  else:
    print "Warning: config not found. Create funnel.config in cwd to enable configurations. Using defaults instead."
    return {
      "build_dir": "build",
      "404type": "file",
      "404name": "404.html",
      "author": "Anonymous",
      "blog": "off",
      "pages": "on"
    }

def get_thing(root, folder, name):
  fn = get_filename(root, folder, name)
  if fn is None:
    raise NotFound

  with open(fn) as f:
    text = f.read()

  return parse_all(text)

# lol, this could be massive.
# there's a your mom joke somewhere in there.
def compile_blog_posts(root, folder):
  """Compiles all the blog posts together from root/folder. Since many
  blog posts could get messy. What we do is we allow the posts to be named as

      <tag that is ignored>-postid.md

  The tag that's ignored could be something like 01, or 001. For easy sorting
  with file managers. The tag is optional. If there's no tag, there should be no
  `-` as well.

  This function returns a list, ordered from newest to oldest. The datetime
  information is either specified "date" meta in a post. If that's not
  available, it falls back to the creation time based on the file system. (in
  that case, only the date portion is used.)

  The list returned consists of blog posts in the format of (meta, html).
  Sections are not allowed in blog posts.

  Metas of blogposts will contain at least a dates and a postid field. You
  should also put title, author, and so forth if you incline. author could also
  be placed in global config.

  date meta format for a post is yyyy-mm-dd hh:mm (24hrs) or yyyy-mm-dd
  """
  posts = []
  for fn in os.listdir(os.path.join(root, folder)):
    _tmp = fn.rsplit(".", 1)
    if len(_tmp) > 1 and _tmp[1] in ACCEPTED_EXTENSIONS:
      _tmp = _tmp[0].split("-", 1)
      if len(_tmp) > 1:
        postid = _tmp[1]
      else:
        postid = _tmp[0]

      # Heh. Hack. But that should be okay. If we want we could easily separate
      # this out again.
      meta, content = get_thing(root, folder, fn.rsplit(".", 1)[0])
      if "main" not in content:
        raise ValueError("Blog posts cannot have sections!")
      html = content["main"]

      if "date" not in meta:
        meta["date"] = datetime.fromtimestamp(os.path.getctime(os.path.join(root, folder, fn)))
      else:
        # We use some "heuristics" here.. (aka wild ass guess)
        meta["date"] = meta["date"].strip()
        if len(meta["date"].split(" ")) > 1:
          meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d %H:%M")
        else:
          meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d")

      meta["postid"] = postid

      posts.append((meta, html))

  posts.sort(key=lambda p: p[0]["date"], reverse=True)
  return posts

def create_flask_app(root):
  """Creates the funnel flask app and sets up everything so that running it
  would start a preview server.
  """
  from flask import Flask, abort, redirect, url_for, render_template, g
  from math import ceil

  # TODO: Yay. unix hack. Someone fix that
  if root == ".":
    template_folder = os.path.join(os.getcwd(), "templates")
    static_folder = os.path.join(os.getcwd(), "static")
  elif not root.startswith("/"):
    template_folder = os.path.join(os.getcwd(), root, "templates")
    static_folder = os.path.join(os.getcwd(), root, "static")
  else:
    template_folder = os.path.join(root, "templates")
    static_folder = os.path.join(root, "static")

  app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
  config = get_config(root)

  app.jinja_env.autoescape = False

  # This looks inefficient...
  # also seems like bad practise? With globals and all...
  def update_posts():
    if config.get("blog", "off").lower() == "on":
      g.all_posts = compile_blog_posts(root, "posts")
      # We need to inject the author into meta
      if "author" in config:
        for meta, html in g.all_posts:
          if "author" not in meta:
            meta["author"] = config["author"]

      # We also need quick look up in case the blog is HUGE.
      g.postid_to_index = {post[0]["postid"]: i for i, post in enumerate(g.all_posts)}

      g.posts_per_page = float(config.get("posts_per_page", 10.0))
      g.total_pages = int(ceil(len(g.all_posts) / g.posts_per_page))

      # It's late like 1:48 (gonna be 3.. daylight savings)
      # I'M SORRY THAT IT HAS TO COME THIS.
      # I need to allow the build script to see these stupid things.
      # So we're gonna stick this shit into the config
      app.config["total_pages"] = g.total_pages
      app.config["postids"] = g.postid_to_index.keys()


  @app.before_request
  def before_request():
    update_posts()
    app.jinja_env.globals["generated"] = datetime.now()
    app.jinja_env.globals["config"] = config

  if config.get("pages", "on").lower() == "on":
    @app.route("/")
    def home():
      return redirect(url_for("page", name="home"))

    @app.route("/<name>/")
    def page(name):
      try:
        meta, content = get_thing(root, "pages", name)
      except NotFound:
        return abort(404)
      else:
        template = meta.get("template", config.get("template", "page.html"))
        return render_template(template, name=name, title=meta.pop("title", None), meta=meta, **content)
  else:
    @app.route("/")
    def home():
      return redirect(url_for("blog", current_page=1))

  if config.get("blog", "off").lower() == "on":
    @app.route("/blog/")
    @app.route("/blog/page/<int:current_page>.html")
    def blog(current_page=1):
      min_index = int((current_page - 1) * g.posts_per_page)
      max_index = int(current_page * g.posts_per_page)

      posts = g.all_posts[min_index:max_index]

      previous_page = int(current_page - 1)
      if previous_page <= 0:
        previous_page = None

      next_page = int(current_page + 1)
      if next_page > g.total_pages:
        next_page = None

      return render_template("blog.html", posts=posts, all_posts=g.all_posts, current_page=current_page, previous_page=previous_page, next_page=next_page, total_pages=g.total_pages)

    @app.route("/blog/<postid>.html")
    def post(postid):
      meta, html = g.all_posts[g.postid_to_index[postid]]

      return render_template("post.html", content=html, **meta)

    if "rss" in config:
      @app.route(config["rss"])
      def rss():
        return render_template("rss.xml", all_posts=g.all_posts)

  if "404" in config:
    @app.route((config["404"]))
    def not_found():
      return render_template("404.html")

  return app

def preview(root):
  if not root:
    root = "."

  app = create_flask_app(root)
  app.run(debug=True, host="", use_reloader=False)

def build(root):
  import os
  import os.path

  from funnel_frozen_flask import Freezer

  if not root:
    root = "."

  app = create_flask_app(root)
  freezer = Freezer(app)

  @freezer.register_generator
  def page():
    for fn in os.listdir(os.path.join(root, "pages")):
      if fn.startswith("404"):
        continue

      _tmp = fn.rsplit(".", 1)
      if len(_tmp) == 1:
        yield {"name": _tmp[0]}
      else:
        if _tmp[1] in ACCEPTED_EXTENSIONS:
          yield {"name": _tmp[0]}

  config = get_config(root)
  if config.get("blog", "off").lower() == "on":
    @freezer.register_generator
    def blog():
      for i in xrange(1, app.config["total_pages"]+1):
        yield {"current_page": i}

    @freezer.register_generator
    def post():
      for postid in app.config["postids"]:
        yield {"postid": postid}

  app.config["FREEZER_DESTINATION"] = config["build_dir"]
  app.config["FREEZER_DESTINATION_IGNORE"] = (".git*", "CNAME")

  # Custom frozen flask stuff
  app.config["FUNNEL_ROOT"] = root
  freezer.freeze()

if __name__ == "__main__":
  preview()
