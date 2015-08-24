Funnel
======

[![Build Status](https://travis-ci.org/shuhaowu/Funnel.svg?branch=master)](https://travis-ci.org/shuhaowu/Funnel)

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

Reference site: https://shuhaowu.com
Reference site source: https://github.com/shuhaowu/shuhaowu.github.com/tree/master

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

 - A full featured blog generator.
 - A full featured site generator.

It should provide just enough that you can do whatever you want with your
templates.

Getting started
---------------

You need the following directory structure to start with Funnel:

    pages/        - Only if static pages are enabled
    posts/        - Only if blogs are enabled
    templates/    - Always
      page.html   - Only if static pages are enabled
      post.html   - Only if blog is enabled
      blog.html   - Only if blog is enabled
      rss.xml     - Only if blog is enabled.
    static/       - Always
    funnel.config - Optional, but recommended

The `pages` directory contains the markdown source for the static pages. The id
of these pages will be the filename without the .md extension. `home.md` is
required as it will be the landing page of the site ("http://yoursite.com/" and
"http://yoursite.com/home/" will both be the same thing).

Any other pages can be accessed by "http://yoursite.com/<id>/" (your files would be named <id>.md)

The `posts` directory contains the markdown source of blog posts (if enabled).
Since people might want to order the posts in her file manager, funnel ignores
everything before the first `-`. That is to say, you can name your files like
`001-blogpost1.md` and the id of the post would be `blogpost1` as oppose to
`001-blogpost1`.

The url to access any particular blog post is http://yoursite.com/blog/<id>.html
and the url to access the front page of the blog is http://yoursite.com/blog/.
For pagination, the page number i is accessible via
`http://yoursite.com/blog/page/<i>.html`

### Markdown Style ###

To write a blogpost/a page, you use a standard markdown file with HTTP style
headers.

    title: The title of the page
    somethinguseful: yay!

    My page
    =======

    Hello Turtles!

The first blank line is the separator between the meta infomation and the page
content. The page content is then compiled into html. `title` is required for
pages.

Although this probably is not usually used, but funnel will detect to see if
your meta value is a python data type and convert them properly. For example,
`someint: 1` will convert the value of `someint` to 1 as oppose to `u"1"`.

Similarly, `somelist: [1, 2, "yay"]` will be converted into a list with those
entries as well. As an example, you can do:

    bool: on
    list: [1, 2, 3]
    i: 1
    s: yay strings

and have it generate the following dictionary:

    {
        "bool": True,
        "list": [1, 2, 3],
        "i": 1,
        "s": "yay strings"
    }

Markdown itself can have sections, such as the following:

    title: A page

    === section1 ===

    Section 1 *content*

    === section1 ===

    === section2 ===

    Section 2 **content**

    === section2 ===

Markdown is enclosed in `=== sectionname === \n .... \n === sectionname ===`.
These will be accessible as different variables in templates. 

Note that only pages can have sections!

### Templates ###

`post.html` is used to render static pages and will receive the following
variables:

 - `main`: The html of the markdown file of the corresponding page.
 - `title`: The title as specified in the meta portion of the markdown file.
 - `name`: The id of the page (so the filename of the markdown file with out its extension)
 - `meta`: Any other meta information in a dictionary as written in the meta
           portion of the markdown file.

However, if your page contains sections, main will not be passed, the names of
your sections will. For example, if you have `=== section1 ===` and 
`=== section2 ===`, the variable `section1` and `section2` will be passed into
the template.

`blog.html` is used to render the main page of the blog (and page 2.. page
3...). It should display multiple posts (10 posts will be given to you by
default).

 - `posts`: A list of 2 tuples contain (meta, html). Where meta is the
            meta in a dictionary and html is the markdown compiled html. This
            is a limited set containing only the posts that should be rendered
            on this page only.
 - `all_posts`: This is the list of **ALL published** posts in the 2 tuple 
   format.
 - `current_page`: The current page number as an integer.
 - `next_page`: The next page number as an integer.
 - `previous_page`: The previous page number as an integer.
 - `total_pages`: The total number of pages as an integer.

`post.html` is the template used to render individual posts. It receives:

 - `content`: The content of the post as html.
 - `author`: The name of the author. Defaults to the author in funnel.config,
             but each post could override by specifying `author` in the meta.
 - `date`: The datetime when the post is written/published. Defaults to the
           creation time of the file. This is inheritantly unreliable so I
           recommend you to override by specifying `date` in the meta of the post.
 - `published`: if this post is published or not. This is specified by you in 
   the meta of each post or it is True by default.
 - Any other meta will be passed directly into the page. So if you have a meta
   as `somethinguseful`, you can access it like that in jinja2 (i.e. `{{ somethinguseful }}`)

`rss.xml` is for the RSS file (you need to enable this in your config file by
specifying rss: /path/to/rss). It receives one variable:

 - `all_posts`: List of all the posts in the 2 tuple format described above. It
                is your responsibility to not list all of them (commonly done via
                `{{ all_posts[:20] }}`)

The `static` directory contains all the static files. So all of your javascripts,
images, stylesheets and so forth goes here. You can access this folder as is
at http://yoursite.com/static/....

If you need an example, please checkout the reference implementation at:
https://github.com/shuhaowu/shuhaowu.github.com/tree/src

Lastly, for static pages, you can use a different template to render. In the
meta of a page, you can specify `template: yourtemplate.html`, and funnel will
use yourtemplate.html to render that page instead of page.html.

Commandline Usage
-----------------

To install, you need libyaml-dev. After that, you can simply run:

    # python setup.py install

After that you should have `funnel` as a commandline utils!

`funnel` should give you all the options.
