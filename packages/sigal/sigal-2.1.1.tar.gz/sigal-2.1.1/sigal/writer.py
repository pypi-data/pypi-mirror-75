# Copyright (c) 2009-2020 - Simon Conseil
# Copyright (c)      2013 - Christophe-Marie Duquesne
# Copyright (c)      2018 - Edwin Steele

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

import imp
import logging
import os
import sys
import types
from distutils.dir_util import copy_tree

import jinja2
from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PrefixLoader
from jinja2.exceptions import TemplateNotFound

from . import signals
from .utils import url_from_path

THEMES_PATH = os.path.normpath(os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'themes'))


class AbstractWriter:
    template_file = None

    def __init__(self, settings, index_title=''):
        self.settings = settings
        self.output_dir = settings['destination']
        self.theme = settings['theme']
        self.index_title = index_title
        self.logger = logging.getLogger(__name__)

        # search the theme in sigal/theme if the given one does not exists
        if not os.path.exists(self.theme) or \
                not os.path.exists(os.path.join(self.theme, 'templates')):
            self.theme = os.path.join(THEMES_PATH, self.theme)
            if not os.path.exists(self.theme):
                raise Exception("Impossible to find the theme %s" % self.theme)

        self.logger.info("Theme  : %s", self.theme)
        theme_relpath = os.path.join(self.theme, 'templates')
        default_loader = FileSystemLoader(os.path.join(THEMES_PATH, 'default',
                                                       'templates'))

        # setup jinja env
        env_options = {'trim_blocks': True, 'autoescape': True}
        try:
            if tuple(int(x) for x in jinja2.__version__.split('.')) >= (2, 7):
                env_options['lstrip_blocks'] = True
        except ValueError:
            pass

        env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader(theme_relpath),
                default_loader,  # implicit inheritance
                PrefixLoader({'!default': default_loader})  # explicit one
            ]),
            **env_options
        )

        # handle optional filters.py
        filters_py = os.path.join(self.theme, 'filters.py')
        if os.path.exists(filters_py):
            mod = imp.load_source('filters', filters_py)
            for name in dir(mod):
                if isinstance(getattr(mod, name), types.FunctionType):
                    env.filters[name] = getattr(mod, name)

        try:
            self.template = env.get_template(self.template_file)
        except TemplateNotFound:
            self.logger.error('The template %s was not found in template folder %s.',
                              self.template_file, theme_relpath)
            sys.exit(1)

        # Copy the theme files in the output dir
        self.theme_path = os.path.join(self.output_dir, 'static')
        copy_tree(os.path.join(self.theme, 'static'), self.theme_path)

    def generate_context(self, album):
        """Generate the context dict for the given path."""

        from . import __url__ as sigal_link
        self.logger.info("Output album : %r", album)
        return {
            'album': album,
            'index_title': self.index_title,
            'settings': self.settings,
            'sigal_link': sigal_link,
            'theme': {'name': os.path.basename(self.theme),
                      'url': url_from_path(os.path.relpath(self.theme_path,
                                                           album.dst_path))},
        }

    def write(self, album):
        """Generate the HTML page and save it."""
        context = self.generate_context(album)
        signals.before_render.send(context)
        page = self.template.render(**context)
        output_file = os.path.join(album.dst_path, album.output_file)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page)


class AlbumListPageWriter(AbstractWriter):
    """Generate an html page for a directory of albums"""
    template_file = "album_list.html"


class AlbumPageWriter(AbstractWriter):
    """Generate html pages for a directory of images."""
    template_file = "album.html"
