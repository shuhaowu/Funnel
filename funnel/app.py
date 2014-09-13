# This file is part of Funnel.
#
# Funnel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Funnel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Funnel.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import

from datetime import datetime
import os

from flask.ext.frozen import Freezer
from watchdog.observers import Observer

from . import utils
from .blog import Blog


def create_flask_app(config):
  """Creates a funnel flask app.

  This creates a preview server, of which we could use to build the
  static website.

  Returns the app and a file system observer if there is one
  """

  from flask import Flask, abort, redirect, url_for, render_template

  root = config["_root"]

  template_folder = config.get("template_folder") or os.path.join(root, "templates")
  static_folder = config.get("static_folder") or os.path.join(root, "static")

  app = Flask("funnel", template_folder=template_folder, static_folder=static_folder)
  app.jinja_env.autoescape = False

  @app.before_request
  def before_request():
    app.jinja_env.globals["generated"] = datetime.now()
    app.jinja_env.globals["config"] = config

  if config.get("pages", True):
    @app.route("/")
    def home():
      return redirect(url_for("page", name="home"))

    @app.route("/<name>/")
    def page(name):
      try:
        meta, content = utils.get_content(config, "pages", name)
      except utils.NotFound:
        return abort(404)
      else:
        template = meta.get("template", config.get("template", "page.html"))
        return render_template(template, name=name, title=meta.pop("title", None), meta=meta, **content)
  elif config.get("blog", False):
    @app.route("/")
    def home():
      return redirect(url_for("blog", current_page=1))

  observer = None
  if config.get("blog", False):
    # a little bit weird that a Blog is also a FileSystemEventHandler
    blog_posts = Blog(config)
    observer = Observer()
    observer.schedule(blog_posts, blog_posts.path, recursive=True)
    app.blog = blog_posts
    app.observer = observer

    @app.route("/blog/")
    @app.route("/blog/page/<int:current_page>.html")
    def blog(current_page=1):
      previous_page = current_page - 1
      previous_page = None if previous_page <= 0 else previous_page

      next_page = current_page + 1
      next_page = None if next_page > blog_posts.total_pages else next_page

      return render_template(
        "blog.html",
        posts=blog_posts.posts_on_page(current_page),
        all_posts=blog_posts.published,
        current_page=current_page,
        previous_page=previous_page,
        next_page=next_page,
        total_pages=blog_posts.total_pages
      )

    @app.route("/blog/<postid>.html")
    def post(postid):
      try:
        meta, html = blog_posts.get_post_by_id(postid)
      except KeyError:
        return abort(404)

      return render_template("post.html", content=html, meta=meta, **meta)

    if "rss" in config:
      @app.route(config["rss"])
      def rss():
        return render_template("rss.xml", all_posts=blog_posts.published)

  if "404" in config:
    @app.route(config["404"])
    def not_found(e=None):
      return render_template("404.html")

  return app


def freeze_flask_app(app, config, target):
  target = os.path.abspath(target)
  freezer = Freezer(app)

  @freezer.register_generator
  def page():
    for fn in os.listdir(os.path.join(config["_root"], "pages")):
      if fn.startswith("404"):
        continue

      _tmp = fn.rsplit(".", 1)
      if len(_tmp) == 1:
        yield {"name": _tmp[0]}
      else:
        if _tmp[1] in utils.ACCEPTED_EXTENSIONS:
          yield {"name": _tmp[0]}

  if config["blog"]:
    @freezer.register_generator
    def blog():
      for i in xrange(1, app.blog.total_pages + 1):
        yield {"current_page": i}

    @freezer.register_generator
    def post():
      for postid in app.blog.postid_to_index.keys():
        yield {"postid": postid}

  app.config["FREEZER_DESTINATION"] = target
  app.config["FREEZER_DESTINATION_IGNORE"] = (".git*", "CNAME")
  freezer.freeze()
