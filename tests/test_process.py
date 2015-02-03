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
from resumepy import process_html
from resumepy import process_pdf
from resumepy import process_text
from resumepy import resumepy_path


class ResumepyProcessTest(unittest.TestCase):
    """Test the elements of process.py"""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.cwd = os.getcwd()
        self.yaml = """contact:
  name: Jane Doe
  address: 555 Beverly Hills Blvd.
  city: Beverly Hills
  state: CA
  zip: 90210
  email: jane@example.com
  phone: 555.555.5555
  jobtitle: Astronaut
website:
  label: mysite
  link: 'http://mysite.com'
objective:
  Reclaim Mars from invaders.
work:
  - organization: European Space Agency
    start: Fall 2056
    stop: Spring 2093
    position: Captain
    location: Space
    notes:
      - Destroyed alien battleship
      - Recovered from engine failure
  - organization: McDonald's
    start: July 2012
    stop: January 2014
    position: Assistant to the Regional Manager
    location: Detriot
    notes:
      - Record for the fastest cheeseburger made
      - Employee of the year
      - Helped lead an amazing team
        """
        self.resume = yaml.load(self.yaml)

        # put bad character (for LaTeX) if yaml
        # the `&` in the email field
        self.yaml_bad = """contact:
  name: Jane Doe
  address: 555 Beverly Hills Blvd.
  city: Beverly Hills
  state: CA
  zip: 90210
  email: jane@example.com & jand@another.net
  phone: 555.555.5555
  jobtitle: Astronaut
objective:
  Reclaim Mars from invaders.
work:
  - organization: European Space Agency
    start: Fall 2056
    stop: Spring 2093
    position: Captain
    location: Space
    notes:
      - Destroyed alien battleship
      - Recovered from engine failure
  - organization: McDonald's
    start: July 2012
    stop: January 2014
    position: Assistant to the Regional Manager
    location: Detriot
    notes:
      - Record for the fastest cheeseburger made
      - Employee of the year
      - Helped lead an amazing team
        """
        self.resume_bad = yaml.load(self.yaml_bad)

        os.chdir(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        os.chdir(self.cwd)

    def test_process_html_created(self):
        """* test_process_html_created -- build/html/resume.html created"""
        process_html(self.resume,
                     os.path.join(resumepy_path, 'data', 'templates'))
        self.assertTrue(os.path.exists('build/html/resume.html'))

    def test_process_pdf_bad(self):
        """* test_process_pdf_bad -- bad LaTeX character"""
        with self.assertRaises(Exception):
            process_pdf(self.resume_bad,
                        os.path.join(resumepy_path, 'data', 'templates'),
                        'template.tex')

    def test_process_pdf_created(self):
        """* test_process_pdf_created -- build/pdf/resume.pdf created"""
        process_pdf(self.resume,
                    os.path.join(resumepy_path, 'data', 'templates'),
                    'template.tex')
        self.assertTrue(os.path.exists('build/pdf/resume.pdf'))

    def test_process_text_created(self):
        """* test_process_text_created -- build/pdf/resume.txt created"""
        process_text(self.resume,
                     os.path.join(resumepy_path, 'data', 'templates'))
        self.assertTrue(os.path.exists('build/text/resume.txt'))
