#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.

"""
Test command line interface for resumepy.
"""

from unittest import TestCase

import os
import tempfile
import shutil

from resumepy import create_parser
from resumepy import FileError


class CommandLineTestCase(TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """
    def setUp(self):
        self.parser = create_parser()

        self.tempdir = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        os.chdir(self.tempdir)

        # write file, content does not matter
        with open('file.yml', 'w') as f:
            f.write('testing')

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        os.chdir(self.cwd)

    def test_with_help_arg(self):
        """
        commandline: test_with_help_arg()
        """
        with self.assertRaises(SystemExit):
            self.parser.parse_args('-h'.split())

    def test_yaml_input_does_not_exist(self):
        """
        commandline: test_yaml_input_does_not_exist()
        """
        with self.assertRaises(FileError):
            self.parser.parse_args('-f file2.yml -o pdf'.split())

    def test_html_output(self):
        """
        commandline: test_html_output()
        """
        args = self.parser.parse_args('-f file.yml -o html'.split())

        self.assertEqual(args.file, 'file.yml')
        self.assertEqual(args.output, 'html')

    def test_pdf_output(self):
        """
        commandline: test_pdf_output()
        """
        args = self.parser.parse_args('-f file.yml -o pdf'.split())

        self.assertEqual(args.file, 'file.yml')
        self.assertEqual(args.output, 'pdf')

    def test_txt_output(self):
        """
        commandline: test_txt_output()
        """
        args = self.parser.parse_args('-f file.yml -o txt'.split())

        self.assertEqual(args.file, 'file.yml')
        self.assertEqual(args.output, 'txt')
