# resumepy

Python package for resumes: YAML input to HTML, PDF, or TEXT output.

## notes

* Tested on Ubuntu 14.04 using Python 2.7 and 3.4 with TeXLive 2013

## install


### Ubuntu 14.04

1. Create a virtualenv, *using Python 2.7*:

``` bash

    $ mkvirtualenv resumepy_git

```

or, *using Python 3.4*:


``` bash

    $ mkvirtualenv resumepy_git -p /usr/bin/python3

```


2. Install, from github, using pip

``` bash

    (resumepy_git):~$ pip install git+git://github.com/cstrelioff/resumepy

```

3. A quick test, get the script help:

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

