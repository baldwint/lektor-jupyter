# -*- coding: utf-8 -*-
import os.path

from weakref import ref as weakref
from markupsafe import Markup

from lektor.pluginsystem import Plugin
from lektor.types import SelectType
from lektor.context import get_ctx

import nbformat
from nbconvert import HTMLExporter

def notebook_to_html(text, record=None):

    # construct full path to the notebook (in same dir)
    directory,contents_lr = os.path.split(record.source_filename)
    notebook_path = os.path.join(directory,text)

    # verify that the named notebook is among the attachments
    for att in record.attachments:
        if att.attachment_filename == notebook_path:
            break
    else:
        raise RuntimeError("Couldn't find notebook file")

    # render it
    with open(notebook_path) as fl:
        nb = nbformat.read(fl, as_version=4)

    exporter = HTMLExporter()
    exporter.template_file = 'basic'

    body,resources = exporter.from_notebook_node(nb)

    return body,resources


class Notebook(object):

    def __init__(self, source, record=None):
        self.source = source
        self.__record = weakref(record) if record is not None else lambda: None
        self.__cached_for_ctx = None
        self.__html = None
        self.__meta = None

    def __bool__(self):
        return bool(self.source)

    def __render(self):
        # When the markdown instance is attached to a cached object we can
        # end up in the situation where the context changed from the time
        # we were put into the cache to the time where we got referenced
        # by something elsewhere.  In that case we need to re-process our
        # markdown.  For instance this affects relative links.
        if self.__html is None or \
           self.__cached_for_ctx != get_ctx():
            self.__html, self.__meta = notebook_to_html(
                self.source, self.__record())
            self.__cached_for_ctx = get_ctx()

    @property
    def meta(self):
        self.__render()
        return self.__meta

    @property
    def html(self):
        self.__render()
        return Markup(self.__html)

    def __getitem__(self, name):
        return self.meta[name]

    def __unicode__(self):
        self.__render()
        return self.__html

    def __html__(self):
        self.__render()
        return Markup(self.__html)

class NotebookDescriptor(object):

    def __init__(self, source):
        self.source = source

    def __get__(self, obj, type=None):
        # descriptor protocol! explanation here:
        # https://gist.github.com/chrisbeaumont/5758381
        if obj is None:
            return self
        return Notebook(self.source, record=obj)

class JupyterType(SelectType):
    widget = 'select'

    def value_from_raw(self, raw):
        return NotebookDescriptor(raw.value or u'')

class JupyterPlugin(Plugin):
    name = u'jupyter'
    description = u'Embed Jupyter notebooks in Lektor pages.'

    def on_setup_env(self):
        self.env.add_type(JupyterType)
