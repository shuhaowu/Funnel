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

Reference site: http://shuhaowu.com
Reference site source: https://github.com/shuhaowu/shuhaowu.github.com/tree/src

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
 - A very very very crude skeleton site generation and github pages deploy
   script and a very crude CLI.

What funnel is NOT:

 - A full featured blog generator.
 - A full featured site generator.

Install
-------

Funnel depends on the Flask stack. It also depend on a library called
Frozen-Flask. However, you do not need to install Frozen-Flask as a specially
modified version is included.

The simplest way would be getting this and downloading `python setup.py install`.
This would setups funnel and add a command line tool named "funnel".

Right now there is no other way of installing as several hacks are done to make
this actually work...

pip and easy_install is not available until I sort out the mess with the command
line utility.

Getting started
---------------

Funnel's emphasis is that everything should be so simple that you don't need
any special tools to get started. However, a very rudimentary one is included to
get you started generating the basic layout of a site.

To run the script:

    $ funnel generate # This will start generating the directory layout in the cwd.

If you want to generate the directory layout somewhere else, use the following
command:

    $ funnel generate /path/to/your/dir # This is relative if there is no prefixed /

The script will ask you a few questions and it will generate the following layout

    build/ - The resulting HTML page when you build
      CNAME - Only if Github deployment is enabled and CNAME is enabled.
    src/ - The markdown, html source and etc.
      pages/ - Only if static pages are enabled
      posts/ - Only if blog is enabled.
      templates/ - Always
        page.html - Only if static pages are enabled
        post.html - Only if blog is enabled
        blog.html - Only if blog is enabled
        rss.xml - Only if blog is enabled.
      static/ - Always
      funnel.config - Always
      deploy - Only if the github deployment is enabled.

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
For pagination, the page number i is accessible via http://yoursite.com/blog/page<i>.html
(So don't name your blogpost page3).

The `templates` directory contains all the jinja2 templates.

All templates receives 2 variables: `generated` and `config` where `generated`
is `datetime.now()` and `config` is the config file (funnel.config) in a
dictionary format.

The `page.html` template is used to render static pages. There are two variables
that four variables that you should receive:

 - `main`: The html of the markdown file of the corresponding page.
 - `title`: The title as specified in the meta portion of the markdown file.
 - `name`: The id of the page (so the filename of the markdown file with out its extension)
 - `meta`: Any other meta information in a dictionary as written in the meta
           portion of the markdown file.

`blog.html` is used to render the main page of the blog (and page 2.. page 3...).
It should display multiple posts (10 posts will be given to you by default) and some
sort of feature to switch page. You can checkout the [reference implementation](https://github.com/shuhaowu/shuhaowu.github.com/tree/src)'s
blog.html for details. There are six variables this template receives:

 - `posts`: A list of 2 tuples contain (meta, html). Where meta is the
            meta in a dictionary and html is the markdown compiled html. This
            is a limited set containing only the posts that should be rendered
            on this page only.
 - `all_posts`: This is the list of **ALL** posts in the 2 tuple format.
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
 - Any other meta will be passed directly into the page. So if you have a meta
   as `somethinguseful`, you can access it like that in jinja2 (i.e. `{{ somethinguseful }}`)

`rss.xml` is for the RSS file. It receives one variable:

 - `all_posts`: List of all the posts in the 2 tuple format described above. It
                is your responsibility to not list all of them (commonly done via
                `{{ all_posts[:20] }}`)

The `static` directory contains all the static files. So all of your javascripts,
images, stylesheets and so forth goes here. You can access this folder as is
at http://yoursite.com/static/....

If you need an example, please checkout the reference implementation at:
https://github.com/shuhaowu/shuhaowu.github.com/tree/src

Previewing and Building the Pages
---------------------------------

To preview. cd into the directory and do `$ funnel preview`. This will start a
preview server at http://localhost:5000

To build, cd into the directory and do `$ funnel build`. This will build the
pages into static HTML for deployment into `../build` if you followed the
generation script.

If you have a github deploy script, you need to setup the build directory with
the github (making sure that git push and so forth works) and just do
`$ ./deploy` in your src directory.


Advanced Usages
---------------

Funnel provides certain advanced features that would be necessary for some sites.
These features are:

 - Different templates for different pages
 - Python data structure in meta
 - Markdown section/partitioning

### Different Templates ###

To use a different template for a particular page, simply have a meta entry of

    template: mytemplate.html

In this case, templates/mytemplate.html will be used to render instead of page.html

### Advanced meta ###

Although this probably is not usually used, but funnel will detect to see if
your meta value is a python data type and convert them properly. For example,
`someint: 1` will convert the value of `someint` to 1 as oppose to `u"1"`.

Similarly, `somelist: [1, 2, "yay"]` will be converted into a list with those
entries as well.

### Markdown sections ###

For certain pages, you may want to have different sections of the page that is
rendered via markdown. Funnel provides this with sections. A usual funnel md file
looks like following:

    title: A page

    A page
    ======

    Hello World. Text Text Text **Text**.......

A markdown file with sections looks like the following:

    title: A page

    === section1 ===

    Section 1 *content*

    === section1 ===

    === section2 ===

    Section 2 **content**

    === section2 ===

A typical page is rendered via `{{ main }}`. The sectioned file as we've seen
will be using `{{ section1 }}` for the html of section1 and `{{ section2 }}` for
the html of section2.

This means: each section starts with `=== sectionname ===` and ends with the same
thing. Everything in between is the markdown to be compiled to html.

This is done in the reference implementation:

 - Markdown: https://github.com/shuhaowu/shuhaowu.github.com/tree/src/pages/home.md
 - Template: https://github.com/shuhaowu/shuhaowu.github.com/tree/src/templates/homepage.html

 Note that `{{ main }}` is gone and it doesn't have any value associated to it
 unless you have a section named main.