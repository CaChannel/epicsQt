#!/usr/bin/env python

"""
setup.py file for epicsQt
"""
# Use setuptools to include build_sphinx, upload/sphinx commands
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = open('README.rst').read()

setup (name = 'epicsQt',
       version = '1.0.0',
       description = """Qt widgets with epics""",
       long_description = long_description,
       author      = "Xiaoqiang Wang",
       author_email= "xiaoqiangwang@gmail.com",
       url         = "http://github.com/CaChanel/epicsQt/",
       packages    = ["epicsQt"],
       install_requires = ['CaChannel'],
       license     = "BSD",
       platforms   = ["Windows", "Linux", "Mac OS X"],
       classifiers = ['Development Status :: 4 - Beta',
                      'Environment :: X11 Applications :: Qt',
                      'Environment :: MacOS X :: Cocoa',
                      'Environment :: Win32 (MS Windows)',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: BSD License',
                      'Programming Language :: Python :: 2',
                      'Programming Language :: Python :: 3',
                      ],
       )
