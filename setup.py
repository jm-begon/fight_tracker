# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Authors: Jean-Michel Begon
#
# License: BSD 3 clause

from distutils.core import setup

NAME = 'fight_tracer'
VERSION = '0.0.dev'
AUTHOR = "Jean-Michel Begon"
AUTHOR_EMAIL = "jm.begon@gmail.com"
URL = 'https://github.com/jm-begon/fight_traker/'
DESCRIPTION = 'A shell-like fight tracker for DnD 5e'
with open('README.md') as f:
    LONG_DESCRIPTION = f.read()
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.8',
    'Topic :: Utilities',
]

if __name__ == '__main__':
    setup(name=NAME,
          version=VERSION,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          url=URL,
          description=DESCRIPTION,
          long_description=LONG_DESCRIPTION,
          license='BSD3',
          classifiers=CLASSIFIERS,
          platforms='any',
          install_requires=[],
          packages=['fight_tracker', "fight_tracker/events",
                    "fight_tracker/stream_renderer", "fight_tracker/rendering",
                    "fight_tracker/bestiary"],
          )

