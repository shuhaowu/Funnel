Funnel
======

Funnel is an ultra lightweight static site generator written in Python. It
focuses on being lightweight and not telling you what you have to do. With
Funnel, you can:

 - Edit your website using your favourate text editor and Markdown.
 - Theme your website using jinja2.
 - Maintain a blog by simply using a text editor.
 - Output static html files so you can host anywhere.

Licensed under GPLv3. I'm pretty sure that building websites with this do not
require you from putting the website under GPL. So you should have no issues
with that aspect.

Features
--------

The most prominent feature of Funnel is the fact that it has almost no
features. Who needs a [tag cloud](http://pelican.readthedocs.org/en/2.7.2/settings.html#tag-cloud)?
Why do I need such a [complicated settings file](https://pelican.readthedocs.org/en/3.1.1/settings.html#example-settings)?

(Note if you can answer the questions above, you should probably go with Pelican or Jekyll)

What funnel provides:

 - A solid way of converting markdown into themed HTML pages.
 - A solid way to keep track of posts converting them into a paginated blog.
 - A solid templating system (yay Jinja2!)
 - Allow you to do whatever the hell you want (modifying the source code, embed
   Disqus, Gangnum style videos, Google Analytics, MathJax, whatever!)

What funnel is NOT:

 - A full featured blog.
 - A full featured site generator.
 - Pain-free (although I hope to make Funnel pain free soon, see next section)

Funnel feature wishlist on the order of importance:

 - [x] Fork Frozen Flask or whatever so that it doesn't wipe the build directory
       clean after a build. (This gets rid of things like .git and CNAME, which
       is important for a github deploy).
 - [ ] Test the mechanism for disabling blog or pages.
 - [ ] A way to specify image classes for markdown, allowing embedding images
       that looks nice (float left or right, in a container).
 - [ ] Syntax highlighting for code.
 - [ ] A generic auto deploy script and an skeleton generation script.
 - [ ] A more solid meta parser
 - [ ] More test coverage and source code comments

Getting started
---------------

First of all, you need to clone this repository. You can clone it somewhere
either where your site source will live, or somewhere different. Note the 2
important symlinks: `funnelbuild` and `funnelpreview`. The 2 scripts are
symlinked to `build.py` and `funnel.py` and they either builds the site or
runs a preview/debug server.

I recommend that you symlink `funnelbuild` and `funnelpreview` somewhere in your
path so you can use them anywhere.

Now, create the following directories:

  - templates: Where your jinja2 templates live
  - static: Static files, such as css, js, images
  - posts: Blog posts # optional if you disabled blog (disabled by default)
  - pages: Static pages. # optional if you disabled pages (enabled by default)

You probably also want to create a file called `funnel.config` at the root
directory of the site source. There will be some important configurations there.

You now need to create a couple of templates. These are only required when you
enable them. These are jinja2 templates and variables will be passed into them.

Variables that passed to all jinja2 templates:
  - `generated`: The datetime when the site is generated
  - `config`: The config file's content in a dictionary.

Templates that are necessary if enabled.

  - page.html: To display any individual page. (Only if pages are enabled)
  - blog.html: To display the blog home page. (Only if blog is enabled)
  - post.html: To display any individual post. (Only if blog is enabled)
  - rss.xml: To display the rss for the blog. (Only if blog is enabled)
