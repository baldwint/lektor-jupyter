from setuptools import setup

setup(
    name='lektor-jupyter',
    version='0.1',
    author=u'Thomas Baldwin',
    author_email='tkb@sent.com',
    license='MIT',
    py_modules=['lektor_jupyter'],
    entry_points={
        'lektor.plugins': [
            'jupyter = lektor_jupyter:JupyterPlugin',
        ]
    }
)
