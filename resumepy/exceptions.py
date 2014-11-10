#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.

"""exceptions.py

Exceptions for the resumepy packge.
"""


class resumepyException(Exception):
    """Root resumepy Exception."""
    pass


class CreateDirError(resumepyException):
    """Exception raised for error creating directory."""
    pass


class CreateFileError(resumepyException):
    """Exception raised for error creating file."""
    pass


class DirError(resumepyException):
    """Exception raised for error finding directory."""
    pass


class FileError(resumepyException):
    """Exception raised for error finding file."""
    pass

class LaTeXError(resumepyException):
    """Exception raised when running LaTeX."""
    pass
