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
# along with Funnel.  If not, see <http://www.gnu.org/licenses/>.from setuptools import setup
import unittest
import funnel

class FunnelTests(unittest.TestCase):
  def test_parse_meta(self):
    meta = """
    string: bare words!!
    string2: "mrrow"

    # should be ignored

    integer: 1 # just a comment
    list: [42, "whoa", ["really?", 1337]]
    dict: {"meow": 1}
    date: 2013-01-02
    """

    meta = funnel.parse_meta(meta)
    self.assertTrue("string" in meta)
    self.assertEquals("bare words!!", meta["string"])

    self.assertTrue("string2" in meta)
    self.assertEquals("mrrow", meta["string2"])

    self.assertTrue("integer" in meta)
    self.assertEquals(1, meta["integer"])

    self.assertTrue("list" in meta)
    self.assertEquals([42, "whoa", ["really?", 1337]], meta["list"])

    self.assertTrue("dict" in meta)
    self.assertEquals({"meow": 1}, meta["dict"])

    self.assertTrue("date" in meta)
    self.assertEquals("2013-01-02", meta["date"])


  def test_parse_meta_failure(self):
    meta = """
    novalue
    """

    # Currently all values will work as we default to make things strings, so if
    # there is a syntax error for list or whatever.. that will screw with the
    # people using it, but we still want bare words and this is the easiest
    # implementation.

    with self.assertRaises(ValueError):
      funnel.parse_meta(meta)

  def test_parse_content(self):
    # No sections
    md = """
Test 123 *yay*
    """

    content = funnel.parse_content(md)
    self.assertTrue("main" in content)
    self.assertEquals("<p>Test 123 <em>yay</em></p>", content["main"])

    # With sections
    md = """
=== section1 ===

Test 123 *yay*

=== section1 ===

=== section2 ===

Test 321 *yay*

=== section2 ===
    """

    content = funnel.parse_content(md)

    self.assertTrue("section1" in content)
    self.assertEquals("<p>Test 123 <em>yay</em></p>", content["section1"])

    self.assertTrue("section2" in content)
    self.assertEquals("<p>Test 321 <em>yay</em></p>", content["section2"])

  def test_parse_all(self):
    text ="""title: Homepage

Homepage is great, isn't it?

    Markdown code block!!!

> What about a quote?"""

    meta, content = funnel.parse_all(text)
    self.assertTrue("title" in meta)
    self.assertEquals("Homepage", meta["title"])

    self.assertTrue("main" in content)

  def test_parse_no_content(self):
    text = ""
    meta, content = funnel.parse_all(text)
    self.assertEquals({}, meta)
    self.assertEquals({"main": u""}, content)

  def test_parse_meta_only(self):
    text = "title: test"
    meta, content = funnel.parse_all(text)
    self.assertEquals({"title": u"test"}, meta)
    self.assertEquals({"main": u""}, content)

  def test_malformed_section(self):
    text = """title: test

===section===
===notsection===
    """
    with self.assertRaises(ValueError):
      funnel.parse_all(text)


if __name__ == "__main__":
  unittest.main()