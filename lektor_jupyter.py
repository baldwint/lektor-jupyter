# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from lektor.types import SelectType, Type
from lektor.environment import Expression, PRIMARY_ALT

class NotebookSource(object):

    def __init__(self, env, options):
        self.source = Expression(env, 'record.attachments')
        item_key = '{{ this._id }}'
        #item_label = 'what'


class NotebookType(SelectType):
    widget = 'select'

    #def __init__(self, env, options):
    #    Type.__init__(self, env, options)

    def to_json(self, pad, record=None, alt=PRIMARY_ALT):
        rv = Type.to_json(self, pad, record, alt)
        rv['choices'] = [
                ('eeny', {'en': 'EENY'}),
                ('meeny',{'en': 'MEENY'}),
                ('miny', {'en': 'MINY'}),
                    ]
        return rv

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
