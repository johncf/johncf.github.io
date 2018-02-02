#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

THEME = 'minimalxy'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['render_math']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        'markdown.extensions.toc': {},
    },
    'output_format': 'html5',
}

AUTHOR = 'John C F'
SITENAME = 'In Short'
SITEURL = ''

PATH = 'content'
STATIC_PATHS = [ 'analysis' ]

TIMEZONE = 'Asia/Kolkata'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 10
DEFAULT_METADATA = {
    'status': 'draft',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ARCHIVES_SAVE_AS = 'archives.html'
CATEGORIES_SAVE_AS = 'categories.html'
TAGS_SAVE_AS = 'tags.html'

RELATIVE_URLS = False
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'

# Theme customizations
MINIMALXY_LOGO = '01'
#MINIMALXY_FAVICON = 'favicon.ico'
MINIMALXY_CURRENT_YEAR = datetime.now().year

# Author
AUTHOR_INTRO = u'Hello! I’m John.'
AUTHOR_DESCRIPTION = u'Trying to keep things simple.'
AUTHOR_AVATAR = 'https://www.gravatar.com/avatar/3ff0a46f18c8d548fa91c12b922290b6?s=160'

# Comments
REMARKBOX_KEY = 'da0795d2-039b-11e8-86c9-040140774501'

# Social
AUTHOR_TWITTER = 'jcf256'
SOCIAL = (
    ('envelope', 'mailto:john.ch.fr@gmail.com'),
    ('twitter', 'http://twitter.com/' + AUTHOR_TWITTER),
    ('github', 'https://github.com/johncf'),
    ('gitlab', 'https://gitlab.com/johncf'),
)

# Menu
MENUITEMS = (
    ('Archive', '/' + ARCHIVES_SAVE_AS),
)
