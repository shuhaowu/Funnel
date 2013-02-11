from flask import Flask, abort, redirect, url_for, render_template
import markdown
import codecs
import os
from datetime import datetime
import re
import json

try:
  import cStringIO as StringIO
except ImportError:
  import StringIO

app = Flask(__name__)
meta_content_sep_regex = re.compile(os.linesep + r"[~]+" + os.linesep)
section_headers_regex = re.compile(r"(===)\W+(\w+)\W+(===)")
section_body_regex = r"===\W+{name}\W+===(.+)---\W+{name}\W+---"

EXTENSIONS = ["markdown", "md", "mkd", "txt"]

@app.before_request
def before_request():
  app.jinja_env.globals["generated"] = datetime.now()

def get_filename(folder, name):
  for ext in EXTENSIONS:
    filename = "{root}/{folder}/{name}.{ext}".format(root=app.config["ROOT_DIR"], folder=folder, name=name, ext=ext)
    if os.path.exists(filename):
      return filename

  filename = "{root}/{folder}/{name}".format(root=app.config["ROOT_DIR"], folder=folder, name=name)
  return filename if os.path.exists(filename) else None


def simple_meta_parser(text):
  text = StringIO.StringIO(text)
  line_num = 0
  meta = {}
  for line in text:
    line_num += 1
    line = line.strip()
    r = line.split(":", 1)
    if len(r) != 2:
      raise ValueError("Meta parsing failed on line {0}.".format(line_num))
    key = r[0].strip()
    try:
      value = eval(r[1].strip()) # lol
    except (SyntaxError, NameError):
      value = r[1].strip() # lolwut

    meta[key] = value

  return meta

def retrieve_content(folder, name):
  filename = get_filename(folder, name)
  if filename is None:
    return None

  f = codecs.open(filename, mode="r", encoding="utf8")
  text = f.read()
  f.close()

  r = meta_content_sep_regex.split(text, 1)
  if len(r) == 2:
    try:
      meta = json.loads(r[0].strip())
    except ValueError:
      meta = simple_meta_parser(r[0].strip())
    text = r[1].strip()
  else:
    meta = {"title": name}

  section_headers = section_headers_regex.findall(text)
  if len(section_headers) == 0:
    return meta, {"content": text}
  else:
    sections = {}
    for section in section_headers:
      section_name = section[1]
      section_body = re.findall(section_body_regex.format(name=section_name), text, flags=re.S)[0]
      section_body = section_body.strip()
      sections[section_name] = section_body
    return meta, sections

def _display_page(pagename):
  try:
    meta, content = retrieve_content("pages", pagename)
  except IOError:
    return abort(404)
  else:
    for c in content:
      content[c] = markdown.markdown(content[c])
    template = meta.get("template", "website.html")
    if content is None:
      return abort(404)
    return render_template(template, page=pagename, title=meta.pop("title"), meta=meta, **content)

@app.route("/<pagename>/")
def display_page(pagename):
  return _display_page(pagename)

@app.route("/")
def home():
  return redirect(url_for("display_page", pagename="home"))

def get_config(root):
  with open("{0}/config.json".format(root)) as f:
    return json.load(f)

  # Default. Good enough for github deployment.
  return {
    "build_dir" : "build",
    "404type" : "file",
    "404name" : "404.html"
  }

def setup_server(root):
  # Good old global variables. Probably should use some sort of flask env
  # variables, but this is the same.
  app.config["ROOT_DIR"] = root

  config = get_config(root)
  if "404name" in config:
    @app.route(("/{0}".format(config["404name"])) + ("" if config["404type"] == "file" else "/"))
    def display404():
      return _display_page("404")

if __name__ == "__main__":
  import sys
  if len(sys.argv) > 1:
    root = sys.argv[1].strip().rstrip("/")
  else:
    root = "."

  setup_server(root)
  app.run(debug=True, host="")