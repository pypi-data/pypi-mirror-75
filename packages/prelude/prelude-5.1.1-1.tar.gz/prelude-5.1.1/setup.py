# Copyright (C) 2005-2019 CS-SI. All Rights Reserved.
# Author: Yoann Vandoorselaere <yoann.v@prelude-ids.com>
#
# This file is part of the Prelude library.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys, os
from os.path import abspath, exists
import shutil

from distutils.sysconfig import get_python_lib
from distutils.core import setup, Extension

def split_args(s):
    import re
    return re.split("\s+", s.strip())


def get_prefix():
    try:
        return sys.argv[sys.argv.index("--prefix") + 1]
    except ValueError:
        return None


def get_root():
    try:
        return sys.argv[sys.argv.index("--root") + 1]
    except ValueError:
        return ""


def is_system_wide_install():
    return os.access(get_python_lib(), os.W_OK)


def pre_install():
    if not is_system_wide_install():
        sys.argv.extend(["--prefix", "/usr"])


def uninstall():
    if is_system_wide_install():
        prefix = get_prefix()
    else:
        prefix = "/usr"

    for f in "prelude.py", "prelude.pyc", "_prelude.so":
        file = get_root() + "/" + get_python_lib(prefix=prefix) + "/" + f
        exists(file) and os.remove(file)

        file = get_root() + "/" + get_python_lib(plat_specific=True, prefix=prefix) + "/" + f
        exists(file) and os.remove(file)

    sys.exit(0)



commands = {
    "install": pre_install,
    "uninstall": uninstall,
    }

if len(sys.argv) > 1 and sys.argv[1] in commands:
    commands[sys.argv[1]]()

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name="prelude",
      version="5.1.1",
      description="Python bindings for the Prelude Library",
      author="CS GROUP France",
      author_email="support.prelude@csgroup.eu",
      long_description=long_description,
      long_description_content_type="text/x-rst",
      url="https://www.prelude-siem.org",
      license="GPL V2.1",
      py_modules=["prelude"],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: Unix",
      ],
      project_urls={
        "Documentation":"https://www.prelude-siem.org/projects/prelude/wiki",
        "Code": "https://github.com/Prelude-SIEM/libprelude",
        "Issue tracker": "https://www.prelude-siem.org/projects/prelude/issues"
      },
      ext_modules=[Extension("_prelude",
                             ["_prelude.cxx"],
                             extra_compile_args=split_args("-I/usr/include/libprelude"),
                             extra_link_args=split_args("-lpreludecpp -lprelude"))])
