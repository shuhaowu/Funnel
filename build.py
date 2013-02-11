from flask_frozen import Freezer
from previewserver import app, setup_server, get_config
import os
freezer = Freezer(app)

@freezer.register_generator
def display_posts():
  if not os.path.exists("posts"):
    return

  files = os.listdir("{root}/posts".format(root=app.config["ROOT_DIR"]))
  for filename in files:
    if os.path.isfile("{root}/posts/{filename}".format(root=app.config["ROOT_DIR"], filename=filename)):
      name = filename.rsplit(".", 1)[0]
      yield {"postname" : name}

@freezer.register_generator
def display_page():
  files = os.listdir("{root}/pages".format(root=app.config["ROOT_DIR"]))
  for filename in files:
    if filename.startswith("404"):
      continue

    if os.path.isfile("{root}/pages/{filename}".format(root=app.config["ROOT_DIR"], filename=filename)):
      name = filename.rsplit(".", 1)[0]
      yield {"pagename" : name}

if __name__ == "__main__":
  import sys
  if len(sys.argv) > 1:
    root = sys.argv[1].strip().rstrip("/")
  else:
    root = "."

  config = get_config(root)
  app.config["FREEZER_DESTINATION"] = config["build_dir"] if config["build_dir"].startswith("/") else root + "/" + config["build_dir"]
  setup_server(root)
  freezer.freeze()
  print "Build Complete!"
