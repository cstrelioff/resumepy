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
from resumepy import process_html, resumepy_path

class ResumepyProcessHtmlTest(unittest.TestCase):
    """Test the resumepy function process_html."""

    def setUp(self):
        """Setup test."""
        self.tempdir = tempfile.mkdtemp()
        self.yaml = """contact:
  name: Jane Doe
  address: 555 Beverly Hills Blvd.
  city: Beverly Hills
  state: CA
  zip: 90210
  email: jane@example.com
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
        self.resume = yaml.load(self.yaml)

    def tearDown(self):
        """TearDown test."""
        shutil.rmtree(self.tempdir)

    def test_process_html_valid(self):
        """Working process_html call."""
        #print("\ntmpdir: {}\n".format(self.tempdir))
        #print("resume: {}\n".format(self.resume))

        cwd = os.getcwd()
        os.chdir(self.tempdir)
        process_html(self.resume, os.path.join(resumepy_path, 'data', 'templates'))
        self.assertTrue(os.path.exists('build/html/resume.html'))
        
        #print("after process html...\n")
        #print("cwd: {}".format(os.getcwd()))
        #print(" ls . : {}".format(os.listdir('.')))
        #print(" ls build/ : {}".format(os.listdir('build')))
        #print(" ls build/html/ : {}".format(os.listdir('build/html')))

        os.chdir(cwd)




