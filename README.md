Jupyter Notebooks in Lektor CMS
===============================

This plugin provides rudimentary support for embedding
[Jupyter](http://jupyter.readthedocs.io/en/latest/#) notebooks in the
[Lektor](https://www.getlektor.com) static content management system.

Usage
-----

This extension makes available a new field type called `jupyter` which
embeds a Jupyter notebook. To use it, define e.g. in your model ini
file:

```ini
[fields.body]
type = jupyter
source = record.attachments
```

The `source` configuration is mandatory to tell Lektor where to look
for the notebook you want to embed. In the admin interface there will
be a drop-down selector where you choose which notebook you want.

Known shortcomings
------------------

- At the moment, the only valid source for notebooks is
`record.attachments`.
- When the attached notebook is modified, Lektor doesn't know to
  update the page in which it is embedded unless you also change the
  `contents.lr` file.

Pull requests welcome!
