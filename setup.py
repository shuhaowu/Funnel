#!/usr/bin/env python
# This file is part of Funnel.
#
# Funnel is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Funnel is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Funnel.  If not, see <http://www.gnu.org/licenses/>.from setuptools import setup

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