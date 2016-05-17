# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.types import SelectType


class NotebookType(SelectType):
    widget = 'select'

    def value_from_raw(self, raw):
        return raw.value or u''

class JupyterPlugin(Plugin):
    name = u'jupyter'
    description = u'Embed Jupyter notebooks in Lektor pages.'

    def on_setup_env(self):
        self.env.types['jupyter'] = NotebookType

    def on_process_template_context(self, context, **extra):
        def test_function():
            return 'Value from plugin %s' % self.name
        context['test_function'] = test_function
