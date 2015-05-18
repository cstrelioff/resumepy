#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.

"""test_process.py

Test (non-command line) methods in the process.py module.

"""
import unittest

import os
import tempfile
import shutil

import yaml
from resumepy import process_html_resume
from resumepy import process_pdf_resume
from resumepy import process_text_resume
from resumepy import resumepy_path


class ResumepyProcessTest(unittest.TestCase):
    """Test the elements of process.py"""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        os.chdir(self.tempdir)

        self.yaml = os.path.join(resumepy_path, 'data', 'examples', 'example_resume.yml')

        with open(self.yaml) as f:
            self.resume = yaml.load(f)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        os.chdir(self.cwd)

    def test_process_html_resume_created(self):
        """
        process: test_process_html_resume_created()
        """
        process_html_resume(self.resume,
                            os.path.join(resumepy_path, 'data', 'templates'),
                            'template.html')
        self.assertTrue(os.path.exists('build/html/resume.html'))

    def test_process_pdf_resume_created(self):
        """
        process: test_process_pdf_resume_created()
        """
        process_pdf_resume(self.resume,
                           os.path.join(resumepy_path, 'data', 'templates'),
                           'template.tex')
        self.assertTrue(os.path.exists('build/pdf/resume.pdf'))

    def test_process_text_resume_created(self):
        """
        process: test_process_text_resume_created()
        """
        process_text_resume(self.resume,
                            os.path.join(resumepy_path, 'data', 'templates'),
                            'template.txt')
        self.assertTrue(os.path.exists('build/text/resume.txt'))
