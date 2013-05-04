#!/usr/bin/env python

from setuptools import setup

setup(name="Funnel",
      version="0.2",
      description="A simple static website/blog generator.",
      author="Shuhao Wu",
      author_email="shuhao@shuhaowu.com",
      license="GPL",
      url="https://github.com/shuhaowu/funnel",
      py_modules=["funnel", "funnel_frozen_flask"],
      scripts=["funnel"],
      install_requires=["Flask", "markdown"],
      classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
        "Topic :: Internet",
        "Environment :: Console"
      ]
     )