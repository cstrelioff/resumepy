resumepy
========

Python package for resumes: YAML input to HTML, PDF, or TEXT output.

Notes
-----

* Tested on Ubuntu 14.04 using TeXLive 2013

install
-------

* Create a virtualenv

``` bash

    $ mkvirtualencv resumpy_git

```

* Install, from github, using pip

``` bash

    (resumepy_git):~$ pip install git+git://github.com/cstrelioff/resumepy

```

* A quick test:

``` bash

    (resumepy_git):~$ resumepy -h
    usage: resumepy [-h] -f FILE -o {txt,html,pdf} [-t TEMPLATE]
    
    Create resume from yaml file.
    
    optional arguments:
      -h, --help         show this help message and exit
      -f FILE            input yaml file
      -o {txt,html,pdf}  output format
      -t TEMPLATE        local template

```

