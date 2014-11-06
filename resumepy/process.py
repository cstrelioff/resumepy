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

import yaml
import jinja2

from .utils import check_dir
from .utils import check_file
from .utils import copy_file
from .utils import mkdirs

resumepy_path = os.path.abspath(os.path.dirname(__file__))


def create_parser():
    """Create argparse parser and define project paths."""

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


def process_html(resume, templates_path):
    """Process the html version of the resume."""

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    template = env.get_template('template.html')

    print("-- resumepy: creating bootstrap website...")

    data_path = os.path.join(resumepy_path, 'data')
    for d in ['js', 'css', 'fonts']:
        source_dir = os.path.join(data_path, d)
        target_dir = os.path.join('build', 'html', d)
        mkdirs(target_dir)

        for f in os.listdir(source_dir):
            if os.path.isfile(os.path.join(source_dir, f)):
                copy_file(os.path.join(source_dir, f), target_dir)

    with open(os.path.join('build', 'html', 'resume.html'), 'w') as f:
        f.write(template.render(resume))

    cwd = os.getcwd()

    print("-- resumepy: output in {}\n".format(
          os.path.join(cwd, "build", "html")))


def process_pdf(resume, templates_path, template_filename):
    """Process the pdf/LaTeX version of the resume."""
    env = jinja2.Environment(
        block_start_string='%{',
        block_end_string='%}',
        variable_start_string='%{{',
        variable_end_string='%}}',
        loader=jinja2.FileSystemLoader(templates_path))

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
        raise Exception("-- resumepy: pdflatex failed."
                        "   Do you have Tex Live 2013 or 2014 availble?")

    print("-- resumepy: output in {}\n".format(
          os.path.join(cwd, "build", "pdf")))


def process_text(resume, templates_path):
    """Process the text verion of the resume."""
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_path))
    template = env.get_template('template.txt')

    print("-- resumepy: creating text file...")

    mkdirs(os.path.join('build', 'text'))

    with open(os.path.join('build', 'text', 'resume.txt'), 'w') as f:
        f.write(template.render(resume))

    cwd = os.getcwd()
    print("-- resumepy: output in {}\n".format(
          os.path.join(cwd, "build", "txt")))


def main():
    """Entry point for ``resumepy`` script."""

    parser = create_parser()
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
        process_text(resume, templates)
    elif args.output == 'html':
        process_html(resume, templates)
    elif args.output == 'pdf':
        process_pdf(resume, templates, template_file)


if __name__ == '__main__':
    main()
