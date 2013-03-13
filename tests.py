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

if __name__ == "__main__":
  unittest.main()