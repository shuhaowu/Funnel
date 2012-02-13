import flask
import codecs
import markdown
import os
import json
app = flask.Flask(__name__)

EXTENSIONS = ["markdown", "md", "mkd", "txt"]

def getFilename(folder, name):
  for ext in EXTENSIONS:
    filename = "%s/%s.%s" % (folder, name, ext)
    if os.path.exists(filename):
      return filename

  filename = "%s/%s" % (folder, name)
  if os.path.exists(filename):
    return filename
  else:
    return None

def retrieveContent(folder, name):
  filename = getFilename(folder, name)
  if filename is None:
    return None
  f = codecs.open(filename, mode="r", encoding="utf8")
  text = f.read()
  f.close()
  return markdown.markdown(text)

def retrieveMeta(folder, name):
  f = codecs.open("%s/%s.meta" % (folder, name), mode="r", encoding="utf8")
  text = f.read()
  f.close()
  return json.loads(text)

@app.route("/blog/")
def displayBlog():
  return flask.render_template("blog.html")

@app.route("/blog/<postname>/")
def displayPost(postname):
  content = retrieveContent("posts", postname)
  meta = retrieveMeta("posts", postname)
  if content is None:
    return flask.abort(404)
  return flask.render_template("post.html", content=content,
      title=meta.pop("title"), meta=meta)

@app.route("/<pagename>/")
def displayPage(pagename):
  content = retrieveContent("pages", pagename)
  meta = retrieveMeta("pages", pagename)
  if content is None:
    return flask.abort(404)
  return flask.render_template("website.html", content=content,
      title=meta.pop("title"), meta=meta)

@app.route("/")
def home():
  return flask.redirect(flask.url_for("displayPage", pagename="home"))

if __name__ == "__main__":
  app.run(debug=True, host="")
