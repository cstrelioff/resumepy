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

from resumepy import create_parser
from unittest import TestCase

class CommandLineTestCase(TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """
    @classmethod
    def setUpClass(cls):
        parser = create_parser()
        cls.parser = parser

class ResumepyTestCase(CommandLineTestCase):
    def test_with_empty_args(self):
        """
        User passes no args, should fail with SystemExit
        """                                    
        with self.assertRaises(SystemExit):
            args = self.parser.parse_args(''.split())

    def test_with_help_arg(self):
        """
        User passes `-h`, should fail wih SystemExit.
        """
        with self.assertRaises(SystemExit):
            args = self.parser.parse_args('-h'.split())

    def test_good_f_o(self):
        """
        User passes `-f file.yml -o pdf`.
        """
        args = self.parser.parse_args('-f file.yml -o pdf'.split())

        self.assertEquals(args.file, 'file.yml')
        self.assertEquals(args.output, 'pdf')

