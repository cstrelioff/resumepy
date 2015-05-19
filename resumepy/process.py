#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.

"""process.py

Main processing code for resumepy.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.builtins import (ascii, bytes, chr, dict, filter, hex, input,  # noqa
                             int, map, next, oct, open, pow, range, round,
                             str, super, zip)

import os
import argparse
import subprocess
import re

import yaml
import jinja2

from .exceptions import LaTeXError

from .utils import check_file
from .utils import copy_file
from .utils import mkdirs

resumepy_path = os.path.abspath(os.path.dirname(__file__))

# kudos to: http://flask.pocoo.org/snippets/55/
LATEX_SUBS = (
    (re.compile(r'\\'), r'\\textbackslash'),
    (re.compile(r'([{}_#%&$])'), r'\\\1'),
    (re.compile(r'~'), r'\~{}'),
    (re.compile(r'\^'), r'\^{}'),
    (re.compile(r'"'), r"''"),
    (re.compile(r'\.\.\.+'), r'\\ldots'),
)


def escape_tex(value):
    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


def create_parser_letter():
    """Create argparse parser for letter and define project paths."""

    parser = argparse.ArgumentParser(description='Create cover letter from '
                                     'yaml file.')
    parser.add_argument('-f', dest='file', help='input yaml file',
                        type=check_file, required=True)
    parser.add_argument('-o', dest='output', help='output format',
                        choices=['txt', 'pdf'],
                        type=str, required=True)
    parser.add_argument('-s', dest='signature', help='signature png file',
                        type=check_file, required=False, default=None)
    parser.add_argument('-t', dest='template', help='local template',
                        type=check_file, required=False, default=None)

    return parser


def create_parser_resume():
    """Create argparse parser for resume and define project paths."""

    parser = argparse.ArgumentParser(description='Create resume from '
                                     'yaml file.')
    parser.add_argument('-f', dest='file', help='input yaml file',
                        type=check_file, required=True)
    parser.add_argument('-o', dest='output', help='output format',
                        choices=['txt', 'html', 'pdf'],
                        type=str, required=True)
    parser.add_argument('-t', dest='template', help='local template',
                        type=check_file, required=False, default=None)

    return parser


def process_html_resume(resume, templates_path, template_filename):
    """Process the html version of the resume."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    template = env.get_template(template_filename)

    print("-- resumepy: creating html file...")

    mkdirs(os.path.join('build', 'html'))

    with open(os.path.join('build', 'html', 'resume.html'), 'w') as f:
        f.write(template.render(resume))

    cwd = os.getcwd()

    print("-- resumepy: output in {}\n".format(
          os.path.join(cwd, "build", "html")))


def process_pdf_letter(letter, templates_path, template_filename,
                       signature=None):
    """Process the pdf/LaTeX version of the cover letter."""
    env = jinja2.Environment(
        block_start_string='%{',
        block_end_string='%}',
        variable_start_string='%{{',
        variable_end_string='%}}',
        loader=jinja2.FileSystemLoader(templates_path))

    env.filters['escape_tex'] = escape_tex

    template = env.get_template(template_filename)

    mkdirs(os.path.join('build', 'pdf'))

    if signature:
        # copy file to build dir
        copy_file(signature, os.path.join('build', 'pdf'))
        # add signtaure filename to letter data structure for template
        letter['signature'] = signature

    with open(os.path.join('build', 'pdf', 'letter.tex'), 'w') as f:
        f.write(template.render(letter))

    print("-- resumepy_letter: creating pdf...")

    try:
        cwd = os.getcwd()
        os.chdir(os.path.join("build", "pdf"))
        command = ["pdflatex", "-interaction=batchmode", "letter.tex"]
        subprocess.check_call(command)
        os.chdir(cwd)
    except:
        msg = ("\n-- resumepy_letter: pdflatex failed.\n"
               "  * Do you have Tex Live 2013 or 2014 availble?\n"
               "  * Maybe you have special chars (&, $,..) in your yaml file?")

        raise LaTeXError(msg)

    print("-- resumepy_letter: output in {}\n".format(
          os.path.join(cwd, "build", "pdf")))

def process_pdf_resume(resume, templates_path, template_filename):
    """Process the pdf/LaTeX version of the resume."""
    env = jinja2.Environment(
        block_start_string='%{',
        block_end_string='%}',
        variable_start_string='%{{',
        variable_end_string='%}}',
        loader=jinja2.FileSystemLoader(templates_path))

    env.filters['escape_tex'] = escape_tex

    template = env.get_template(template_filename)

    mkdirs(os.path.join('build', 'pdf'))

    with open(os.path.join('build', 'pdf', 'resume.tex'), 'w') as f:
        f.write(template.render(resume))

    print("-- resumepy: creating pdf...")

    try:
        cwd = os.getcwd()
        os.chdir(os.path.join("build", "pdf"))
        command = ["pdflatex", "-interaction=batchmode", "resume.tex"]
        subprocess.check_call(command)
        os.chdir(cwd)
    except:
        msg = ("\n-- resumepy: pdflatex failed.\n"
               "  * Do you have Tex Live 2013 or 2014 availble?\n"
               "  * Maybe you have special chars (&, $,..) in your yaml file?")

        raise LaTeXError(msg)

    print("-- resumepy: output in {}\n".format(
          os.path.join(cwd, "build", "pdf")))


def process_text_resume(resume, templates_path, template_filename):
    """Process the text verion of the resume."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    template = env.get_template(template_filename)

    print("-- resumepy: creating text file...")

    mkdirs(os.path.join('build', 'text'))

    with open(os.path.join('build', 'text', 'resume.txt'), 'w') as f:
        f.write(template.render(resume))

    cwd = os.getcwd()
    print("-- resumepy: output in {}\n".format(
          os.path.join(cwd, "build", "txt")))


def main_letter():
    """Entry point for ``resumepy_letter`` script."""

    parser = create_parser_letter()
    args = parser.parse_args()

    with open(args.file) as f:
        letter = yaml.load(f)

    templates_path = os.path.join(resumepy_path, 'data', 'templates')
    if args.template:
        template_file = args.template
        templates = ['.', templates_path]
    else:
        if args.output == 'pdf':
            template_file = 'letter.{}'.format('tex')
        else:
            template_file = 'letter.{}'.format(args.output)
        templates = templates_path

    if args.output == 'txt':
        process_text_letter(letter, templates, template_file)
    elif args.output == 'pdf' and args.signature:
        process_pdf_letter(letter, templates, template_file, args.signature)
    else:
        process_pdf_letter(letter, templates, template_file)

def main_resume():
    """Entry point for ``resumepy`` script."""

    parser = create_parser_resume()
    args = parser.parse_args()

    with open(args.file) as f:
        resume = yaml.load(f)

    templates_path = os.path.join(resumepy_path, 'data', 'templates')
    if args.template:
        template_file = args.template
        templates = ['.', templates_path]
    else:
        if args.output == 'pdf':
            template_file = 'template.{}'.format('tex')
        else:
            template_file = 'template.{}'.format(args.output)
        templates = templates_path

    if args.output == 'txt':
        process_text_resume(resume, templates, template_file)
    elif args.output == 'html':
        process_html_resume(resume, templates, template_file)
    elif args.output == 'pdf':
        process_pdf_resume(resume, templates, template_file)
