#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.

"""utils.py

Utilities for resumepy.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins import (ascii, bytes, chr, dict, filter, hex, input,  # noqa
                             int, map, next, oct, open, pow, range, round,
                             str, super, zip)

import os
import contextlib
import shutil
import tempfile

from .exceptions import DirError
from .exceptions import FileError

resumepy_path = os.path.abspath(os.path.dirname(__file__))


def check_dir(path):
    """Check that directory exists for argparse."""
    if os.path.exists(path):
        return path
    else:
        raise DirError("Template directory `{}` does not exist.".format(path))


def check_file(file):
    """Check that a file exists for argparse."""
    if os.path.isfile(file):
        return file
    else:
        raise FileError("Unable to find/open `{}`".format(file))


def copy_example():
    """Copy example yaml resume to current working directory."""
    print("-- resumepy: copying example_resume.yml to current directory...")

    src = os.path.join(resumepy_path, "data", "examples", "example_resume.yml")
    copy_file(src, os.getcwd())


def copy_file(src, dest):
    try:
        shutil.copy(src, dest)
    except shutil.Error as e:
        print("Error: {}".format(e))
        print("src: {} dest: {}".format(src, dest))
    except IOError as e:
        print("Error: {}".format(e.strerror))
        print("src: {} dest: {}".format(src, dest))


def mkdirs(path):
    """Make all directories in path.

    Credit
    ------
    Starting ides for this function:

        http://stackoverflow.com/a/18503387
    """
    sub_path = os.path.dirname(path)
    if not os.path.exists(path) and sub_path == '':
        os.mkdir(path)
    elif not os.path.exists(sub_path):
        mkdirs(sub_path)

    if not os.path.exists(path):
        os.mkdir(path)


@contextlib.contextmanager
def make_temp_directory():
    """Context for temporary directories.

    Example
    -------
    with make_temp_directory() as temp_dir:
        <some code>

    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
