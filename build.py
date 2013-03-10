#!/usr/bin/python

if __name__ == "__main__":
  import sys
  import os
  import os.path
  from flask_frozen import Freezer
  from funnel import create_flask_app, ACCEPTED_EXTENSIONS, get_config

  if len(sys.argv) > 1:
    root = sys.argv[1].strip().rstrip("/")
  else:
    root = "."

  app = create_flask_app(root)
  freezer = Freezer(app)

  @freezer.register_generator
  def page():
    for fn in os.listdir(os.path.join(root, "pages")):
      if fn.startswith("404"):
        continue

      _tmp = fn.rsplit(".", 1)
      if len(_tmp) == 1:
        yield {"name": _tmp[0]}
      else:
        if _tmp[1] in ACCEPTED_EXTENSIONS:
          yield {"name": _tmp[0]}

  @freezer.register_generator
  def blog():
    for i in xrange(1, app.config["total_pages"]+1):
      yield {"current_page": i}

  @freezer.register_generator
  def post():
    for postid in app.config["postids"]:
      yield {"postid": postid}

  config = get_config(root)
  app.config["FREEZER_DESTINATION"] = config["build_dir"] if config["build_dir"].startswith("/") else root + "/" + config["build_dir"]
  freezer.freeze()

  if "CNAME" in config:
    with open(os.path.join(app.config["FREEZER_DESTINATION"], "CNAME"), "w") as f:
      f.write(config["CNAME"] + os.linesep)
