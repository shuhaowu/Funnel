from flask_frozen import Freezer
from previewserver import app
import os
import json
with open("config.json") as f:
  config = json.load(f)
app.config["FREEZER_DESTINATION"] = config["build_dir"]
freezer = Freezer(app)

@freezer.register_generator
def displayPost():
  if not os.path.exists("posts"):
    return

  files = os.listdir("posts")
  for filename in files:
    if filename.endswith("meta") and os.path.isfile("posts/%s" % filename):
      name = filename.rsplit(".", 1)[0]
      yield {"postname" : name}

@freezer.register_generator
def displayPage():
  files = os.listdir("pages")
  for filename in files:
    if filename.startswith("404"):
      continue

    if filename.endswith("meta") and os.path.isfile("pages/%s" % filename):
      name = filename.rsplit(".", 1)[0]
      yield {"pagename" : name}

if __name__ == "__main__":
  freezer.freeze()
  print "Build Complete!"
