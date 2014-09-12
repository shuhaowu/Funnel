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

import json
import os
import re

import markdown


class NotFound(LookupError):
  pass


_boolean_map = {
  "yes": True,
  "on": True,
  "true": True,
  "no": False,
  "off": False,
  "false": False,
  True: True,
  False: False,
  1: True,
  0: False,
  "1": True,
  "0": False
}


ACCEPTED_EXTENSIONS = ("markdown", "md", "mkd", "txt")


def boolean_map(v, default=None):
  if default is None:
    return _boolean_map[str(v).lower()]

  return _boolean_map.get(str(v).lower(), _boolean_map[default])


def get_filename(root, folder, name):
  for ext in ACCEPTED_EXTENSIONS:
    fn = os.path.join(root, folder, name + "." + ext)
    if os.path.exists(fn):
      return fn

  # also accepts filename without an extension
  fn = os.path.join(root, folder, name)
  return fn if os.path.exists(fn) else None


def get_content(config, ttype, name):
  fn = get_filename(config["_root"], ttype, name)
  if fn is None:
    raise NotFound

  with open(fn) as f:
    text = f.read()

  return parse(text)


def get_config(root):
  root = os.path.abspath(root)
  if os.path.exists(os.path.join(root, "funnel.config")):
    with open(os.path.join(root, "funnel.config")) as f:
      data = f.read()

    config = parse_meta(data)
  else:
    config = {
      "author": "Anonymous",
      "404": "/404.html",
      "blog": False,
      "pages": True
    }

  config["_root"] = root
  return config


def parse(text):
  """Parses through the text of a file.

  Extracts out meta, content as the return value (in a tuple).

  See parse_meta and parse_content for details.
  """
  # extract out the header information from the markdown content
  text = text.strip().split(os.linesep * 2, 1)
  meta = ""
  content = ""
  if len(text) > 0:
    meta = text[0].strip()

  if len(text) > 1:
    content = text[1].strip()

  return parse_meta(meta), parse_content(content)


def parse_meta(meta):
  """Parses through the meta of a markdown file. The structure is:

      key: value
      key: value # comment
      key: value

      This uses json.loads(). If it fails it will turn it into a string.

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

    # comment or empty line. even though we can't have an empty line
    # due to the fact that we split the text with \n\n
    if not line or line.startswith("#"):
      continue

    # inline comment
    line = line.rsplit("#", 1)[0]
    _temp = line.split(":", 1)
    if len(_temp) != 2:
      raise ValueError("Format of the line is wrong for meta on line {0} with text {1}".format(i, line))

    key = _temp[0].strip()
    value = _temp[1].strip()

    try:
      value = boolean_map(value, None)
    except KeyError:
      try:
        value = json.loads(value)
      except ValueError:
        value = unicode(value)

    m[key] = value

  return m


SECTION_HEADERS_REGEX = re.compile(r"(===)\W*(\w+)\W*?(===)")
SECTION_BODIES_REGEX = r"===\W*?{name}\W*?===(.+)===\W*?{name}\W*?==="


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
