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

from __future__ import absolute_import, division

from datetime import datetime
from math import ceil
import os

import markdown
from watchdog.events import FileSystemEventHandler

from . import utils


class Blog(FileSystemEventHandler):
  def __init__(self, config):
    self.config = config

    self.posts_per_page = config.get("posts_per_page", 10)
    self.total_pages = 0
    self.postid_to_index = dict()

    self.posts = []
    self.published = []
    self.unpublished = []

    self.path = os.path.join(self.config["_root"], "posts")
    self.refresh_blog_posts()

  def refresh_blog_posts(self):
    for fn in os.listdir(self.path):
      _temp = fn.rsplit(".", 1)
      if len(_temp) > 1 and _temp[1] not in utils.ACCEPTED_EXTENSIONS:
        continue

      _temp = _temp[0].split("-", 1)
      if len(_temp) > 1:
        postid = _temp[1]
      else:
        postid = _temp[0]

      meta, content = utils.get_content(self.config, "posts", fn)
      if "main" not in content:
        raise ValueError("Blog posts cannot have sections!")

      html = content["main"]

      if "date" not in meta:
        meta["date"] = datetime.fromtimestamp(os.path.getctime(os.path.join(self.config["_root"], "posts", fn)))
      else:
        meta["date"] = meta["date"].strip()
        if len(meta["date"].split(" ")) > 1:
          meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d %H:%M")
        else:
          meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d")

      meta["postid"] = postid
      meta["filename"] = fn
      # Get the exerpt and the whole thing
      if "excerpt" not in meta:
        # We get the first horizontal rule and before that is the exerpt.
        # That means first horizontal rule will disappear.
        splitted = html.split("<hr />", 1)
        html = "".join(splitted)

        # We set exerpt to 0 anyway if the length of splitted is 1 (no exerpt)
        # this way templates can trust that exerpt has something.
        meta["excerpt"] = splitted[0]
      else:
        meta["excerpt"] = markdown.markdown(meta["excerpt"])

      self.posts.append((meta, html))

    self.posts.sort(key=lambda p: p[0]["date"], reverse=True)

    self.postid_to_index = {}
    for i, (meta, html) in enumerate(self.posts):
      self.postid_to_index[meta["postid"]] = i

      if "author" not in meta and "author" in self.config:
        meta["author"] = self.config["author"]

      meta["published"] = meta.get("published", True)
      if meta["published"]:
        self.published.append((meta, html))
      else:
        self.unpublished.append((meta, html))

    self.total_pages = int(ceil(len(self.published) / self.posts_per_page))

  def posts_on_page(self, page):
    min_index = (page - 1) * self.posts_per_page
    max_index = page * self.posts_per_page

    return self.published[min_index:max_index]

  def get_post_by_id(self, postid):
    return self.posts[self.postid_to_index[postid]]

  _accepted = tuple([""] + ["." + ext for ext in utils.ACCEPTED_EXTENSIONS])

  def on_any_event(self, event):
    # don't want to process directory events
    if event.is_directory:
      return

    srcext = os.path.splitext(event.src_path)[1]
    destext = getattr(event, "dest_path", None)
    if destext is not None:
      destext = os.path.splitext(destext)[1]

    # irrelevant to us if the extension is something we're not interested in
    if srcext not in self._accepted and (destext is None or destext not in self._accepted):
      return

    print "{} changed... rebuilding blog:".format(getattr(event, "dest_path", None) or event.src_path),
    start = datetime.now()
    try:
      self.refresh_blog_posts()
      print datetime.now() - start
    except Exception as e:
      # if we don't catch this the watchdog thread will quit and we will not
      # get any more events.
      print datetime.now() - start
      print "blog failed to rebuild:", e
