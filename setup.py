#!/usr/bin/env python
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

setup(
  name='funnel',
  version='1.0',
  description="A simple static website/blog generator.",
  author="Shuhao Wu",
  author_email="shuhao@shuhaowu.com",
  license="GPL",
  url="https://github.com/shuhaowu/funnel",
  packages=["funnel"],
  scripts=["scripts/funnel"],
  install_requires=requirements,
  classifiers=[
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: Unix",
    "Topic :: Internet",
    "Environment :: Console"
  ]
)
