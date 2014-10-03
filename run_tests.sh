#! /bin/sh
#
# run_tests.sh
# Copyright (C) 2014 Christopher C. Strelioff <chris.strelioff@gmail.com>
#
# Distributed under terms of the MIT license.
#
nosetests -v --with-coverage --cover-package=resumepy --cover-inclusive --cover-erase tests

