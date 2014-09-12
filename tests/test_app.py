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
# along with Funnel.  If not, see <http://www.gnu.org/licenses/>.:
import os
import unittest

from funnel import utils
from funnel.app import create_flask_app


class AppTest(unittest.TestCase):
  def setUp(self):
    self.config = utils.get_config(os.path.join(os.path.dirname(os.path.abspath(__file__)), "teststuff"))

    self.app = create_flask_app(self.config)
    self.app.config["TESTING"] = True
    self.client = self.app.test_client()

    self.app.observer.start()

  def tearDown(self):
    self.app.observer.stop()

  def test_home(self):
    resp = self.client.get("/", follow_redirects=False)
    self.assertEquals(302, resp.status_code)
    self.assertEquals("http://localhost/home/", resp.headers["Location"])

  def test_page(self):
    resp = self.client.get("/home/")
    self.assertEquals(200, resp.status_code)
    self.assertEquals("home\n\n<p>homepage</p>", resp.data)

    resp = self.client.get("/special/")
    self.assertEquals(200, resp.status_code)
    self.assertEquals("special\n\nsection1: <p>section1content</p>\nsection2: <p>section2content</p>", resp.data)

  def test_blog(self):
    resp = self.client.get("/blog/")
    self.assertEquals(200, resp.status_code)
    expected = """
posts: 5
all_posts: 5
current_page: 1
next_page: None
previous_page: None
total_pages: 1
first_post_title: post6
""".strip()
    self.assertEquals(expected, resp.data.strip())

    # gotta recreate the app if we want to do weird things like this
    self.config["posts_per_page"] = 2
    self.app.observer.stop()
    self.app = create_flask_app(self.config)
    self.app.config["TESTING"] = True
    self.client = self.app.test_client()

    resp = self.client.get("/blog/")
    self.assertEquals(200, resp.status_code)
    expected = """
posts: 2
all_posts: 5
current_page: 1
next_page: 2
previous_page: None
total_pages: 3
first_post_title: post6
""".strip()
    self.assertEquals(expected, resp.data.strip())

    resp = self.client.get("/blog/page/2.html")
    self.assertEquals(200, resp.status_code)
    expected = """
posts: 2
all_posts: 5
current_page: 2
next_page: 3
previous_page: 1
total_pages: 3
first_post_title: post3
""".strip()
    self.assertEquals(expected, resp.data.strip())

  def test_post(self):
    resp = self.client.get("/blog/post6.html")
    self.assertEquals(200, resp.status_code)
    expected = """
title: post6
author: Shuhao
content:
<p>post6</p>
""".strip()
    self.assertEquals(expected, resp.data)

  def test_404(self):
    # It's up to you to know how to serve this file. This simply just generate
    # the 404 page at the requested URL.
    resp = self.client.get("/404.html")
    self.assertEquals(200, resp.status_code)
    self.assertEquals("404", resp.data)

  def test_rss(self):
    resp = self.client.get("/rss.xml")
    self.assertEquals(200, resp.status_code)
    self.assertEquals("all_posts: 5", resp.data)
