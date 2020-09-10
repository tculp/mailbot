#!/usr/bin/env python

from setuptools import setup

Description = """/
mailbot
"""

# setup parameters
setup(name='mailbot',
      version='2.0',
      description='Terminal email program',
      # long_description=Description,
      author='Tyler Culp',
      packages=['mailbot'],
      author_email='tylercculp@gmail.com',
      classifiers=["Programming Language :: Python :: 3.5",
                   'Programming Language :: Python',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   "Intended Audience :: End Users/Desktop",
                   ],
      install_requires=[
          'google-api-python-client >= 1.0',
          'oauth2client >= 1.0',
      ],
      entry_points={
                'console_scripts': ['mailbot=mailbot.mailbot:main',
                                    'mailbotd=mailbot.mailbotd:main']
            }
      )
