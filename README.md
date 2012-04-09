Funnel
======

Funnel is a static html website generator using markdown. Users simply edit
the markdown files and the meta files (json) in the posts and pages directory
and run `python build.py` to generate a static html website based on those
files.

Funnel is dependant on markdown (python), flask, and frozen flask.

Howto
=====

Funnel allows you to quickly generate lightweight websites from markdown. After
installing the above, here's how to get started:

 1. Create a new directory somewhere.
 2. `git init`
 3. `git remote add funnel git://github.com/ultimatebuster/Funnel.git`
 4. `git fetch funnel`
 5. `git merge funnel/master`

This gives you the latest version of funnel to work with. Let me introduce the
files that's given to you.

 - `templates/`: A directory where your templates resides. These are standard
   jinja2 templates
 - `pages/`: The markdown file and meta files for each page. You can see there
   is already home.markdown and home.meta. These files are used to construct
   the site.
 - `build.py`: The build script. You can open it up and change
   `app.config["FREEZER_DESTINATION"] = "build"` to a destination of you choice.
   Just replace build with some other path.
 - `previewserver.py`: This fires up a localhost server so you can previous your
   site. Defaults to http://localhost:5000/

Here are some important files/dirs that's not there that's still important.

 - `static/`: This is where you store your css, images, and javascript. To
   reference it from your site, it should be `rootofyoursite/static/*`
 - `posts/`: This is where you write posts for the blog. The blog feature is
   currently still a work in progress. It should be working, but the blog main
   page renderer is not complete, and it's never been tested.

Site specific files are as follows (these files must be presense):

 - `templates/website.html`: The default template to be rendered for any page
   unless overriden by the meta file (explained later)
 - `templates/blog.html`: Blog main page. Not yet available
 - `templates/post.html`: Blog post pages. Not yet available
 - `pages/home.markdown`: The content for the homepage. (Markdown file)
 - `pages/home.meta`: The meta file for the homepage. (JSON file)

Let's have an overview on how funnel's routing works
(excluding the blog as it's N/A).

 1. Funnel looks through your `pages` directory and see all the filenames. The
    filename corresponds to the postfixes to the url. For example,
    http://example.com/about/ will correspond to about.markdown and about.meta.
    Note that the extension must be correct. Markdown files can have the
    extension of "markdown", "md", "mkd", "txt". The meta files must end with
    "meta".
 2. The default page (with the url of http://example.com) is routed to the page
    with the name home. This is why home.markdown and home.meta is required.
 3. The content of home.markdown is examined and compiled into HTML (explained
    in details later) and passed in to the jinja2 template for rendering.
 4. The meta file is converted from its json format to a dictionary and passed
    to the jinja2 template under the variable name `meta`

Let's construct a page for About Us, a common page for many website:

First, you probably want to create a jinja2 template. For this you must refer
to the jinja2 documentations. Then you need to create 2 files, about.markdown
and about.meta under the pages directory.

In about.meta, you need to specify a JSON object. There's 1 attribute that's
required, which is "title". This will be useful to display the title of the page
(example: `<title>{{ title }} - My Site</title>`).

    {
      "title" : "About Us"
    }

The value "About Us" will be passed as `title` to jinja2 (so you can display
using `{{ title }}`). The rest of that JSON object will be passed as a
dictionary of `meta` to jinja2 (in this case `meta == {}`)

Now you can save the file and open up about.markdown. You can just write
whatever markdown you need and that will be compiled to HTML and can be
displayed using `{{ content }}`. Example:

Markdown file:

    About
    =====

    Funnel is awesome!

This will be translated into

    <h1>About</h1>

    <p>Funnel is awesome!</p>

This is stored into the variable `content`. So when you call

    {% autoescape off %}
    {{ content }}
    {% endautoescape %}

The above HTML will be rendered by the browser.

This process can be repeated to create any number of pages. Just make sure you
have a working template.

Now. There are sites where there are parts of the page and not everything can be
done using 1 section. Funnel allows you to do that too. You can pass in multiple
variables to the jinja2 template by specifying sections in the markdown file.
Each section is compiled into HTML and then passed into jinja2.

Markdown File:

    === sectionleft ===
    `Hello, I'm from section left!`
    --- sectionleft ---

    === sectionright ===
    Hello, I'm from section right!
    --- sectionright ---

`=== variablename ===` indicates the start of a section, `--- variablename ---`
indicate the stop of that section. Everything in between will be compiled into
HTML and it will be passed as a variable as the name you specified. For the
example given, `{{ sectionleft }}` will give you
`<p><code>Hello, I'm from section left!</code></p>`. `{{ sectionright }}` will
give you `<p>Hello, I'm from section right!</p>`.

Last feature, in the meta file, you can specify a page to be rendered from a
different template under the templates directory. Example:

    {
      "title" : "About Us",
      "template" : "website2.html"
    }

This will cause our about page to be rendered from `templates/website2.html` as
oppose to `templates/website.html`

Here's a list of all the variables passed into jinja2 by funnel.

 - `generated`: A global variable available for all pages, and all the same. It
   is `datetime.datetime.now()`
 - `page`: The page id (about.markdown will have a page id of `about`)
 - `title`: The title specified in the meta file
 - `meta`: The dictionary as specified in the meta file excluding the title
   attribute.
 - `content`: Not necessarily available. Available if there's a section named
   `content` in the markdown file, or if there's 0 sections specified and the
   whole markdown file is treated as one big section named `content`
