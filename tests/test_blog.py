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

import os
import unittest

from funnel import utils
from funnel.blog import Blog


class BlogTest(unittest.TestCase):
  def setUp(self):
    self.config = utils.get_config(os.path.join(os.path.dirname(os.path.abspath(__file__)), "teststuff"))
    self.blog = Blog(self.config)

  def test_init(self):
    self.assertEquals(6, len(self.blog.posts))
    self.assertEquals(5, len(self.blog.published))
    self.assertEquals(1, len(self.blog.unpublished))

    self.assertEquals("post6", self.blog.posts[0][0]["title"])
    self.assertEquals("post5", self.blog.posts[1][0]["title"])
    self.assertEquals("post4", self.blog.posts[2][0]["title"])
    self.assertEquals("post3", self.blog.posts[3][0]["title"])
    self.assertEquals("post2", self.blog.posts[4][0]["title"])
    self.assertEquals("post1", self.blog.posts[5][0]["title"])

    self.assertEquals("post6", self.blog.published[0][0]["title"])
    self.assertEquals("post4", self.blog.published[1][0]["title"])
    self.assertEquals("post3", self.blog.published[2][0]["title"])
    self.assertEquals("post2", self.blog.published[3][0]["title"])
    self.assertEquals("post1", self.blog.published[4][0]["title"])

    self.assertEquals("post5", self.blog.unpublished[0][0]["title"])

  def test_attributes(self):
    self.assertEquals("post6", self.blog.posts[0][0]["postid"])
    self.assertEquals("post5-unpublished", self.blog.posts[1][0]["postid"])
    self.assertEquals("post4-inferred-excerpt", self.blog.posts[2][0]["postid"])
    self.assertEquals("post3-with-excerpt", self.blog.posts[3][0]["postid"])
    self.assertEquals("post2", self.blog.posts[4][0]["postid"])
    self.assertEquals("post1", self.blog.posts[5][0]["postid"])

    self.assertEquals("2013-08-10 12:50", self.blog.posts[0][0]["date"].strftime("%Y-%m-%d %H:%M"))
    self.assertEquals("2013-07-10 12:50", self.blog.posts[1][0]["date"].strftime("%Y-%m-%d %H:%M"))
    self.assertEquals("2013-06-10 12:50", self.blog.posts[2][0]["date"].strftime("%Y-%m-%d %H:%M"))
    self.assertEquals("2013-05-10 12:50", self.blog.posts[3][0]["date"].strftime("%Y-%m-%d %H:%M"))
    self.assertEquals("2013-04-10 12:50", self.blog.posts[4][0]["date"].strftime("%Y-%m-%d %H:%M"))
    self.assertEquals("2013-03-10 12:50", self.blog.posts[5][0]["date"].strftime("%Y-%m-%d %H:%M"))

    self.assertEquals("post6.md", self.blog.posts[0][0]["filename"])
    self.assertEquals("05-post5-unpublished.md", self.blog.posts[1][0]["filename"])
    self.assertEquals("04-post4-inferred-excerpt.md", self.blog.posts[2][0]["filename"])
    self.assertEquals("03-post3-with-excerpt.md", self.blog.posts[3][0]["filename"])
    self.assertEquals("02-post2.md", self.blog.posts[4][0]["filename"])
    self.assertEquals("01-post1.md", self.blog.posts[5][0]["filename"])

    self.assertEquals("Someone Else", self.blog.posts[4][0]["author"])
    self.assertEquals("<p>test</p>", self.blog.posts[3][0]["excerpt"])
    self.assertEquals("<p>hello world</p>", self.blog.posts[2][0]["excerpt"].strip())
    self.assertEquals(False, self.blog.posts[1][0]["published"])
    self.assertEquals("test", self.blog.posts[0][0]["attribute"])
    self.assertEquals(True, self.blog.posts[0][0]["bool"])

    self.assertEquals("<p>post6</p>", self.blog.posts[0][1].strip())
    self.assertEquals("<p>post5</p>", self.blog.posts[1][1].strip())
    self.assertEquals("<p>hello world</p>\n\n<p>post4</p>", self.blog.posts[2][1].strip())
    self.assertEquals("<p>post3</p>", self.blog.posts[3][1].strip())
    self.assertEquals("<p>post2</p>", self.blog.posts[4][1].strip())
    self.assertEquals("<p>post1</p>", self.blog.posts[5][1].strip())

  def test_methods(self):
    self.config["posts_per_page"] = 2
    self.blog = Blog(self.config)

    post = self.blog.get_post_by_id("post5-unpublished")
    self.assertEquals("post5", post[0]["title"])

    post = self.blog.get_post_by_id("post6")
    self.assertEquals("post6", post[0]["title"])

    self.assertEquals(3, self.blog.total_pages)

    posts = self.blog.posts_on_page(1)
    self.assertEquals(2, len(posts))
    self.assertEquals("post6", posts[0][0]["title"])
    self.assertEquals("post4", posts[1][0]["title"])

    posts = self.blog.posts_on_page(2)
    self.assertEquals(2, len(posts))
    self.assertEquals("post3", posts[0][0]["title"])
    self.assertEquals("post2", posts[1][0]["title"])

    posts = self.blog.posts_on_page(3)
    self.assertEquals(1, len(posts))
    self.assertEquals("post1", posts[0][0]["title"])
