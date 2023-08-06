[![PyPI version](https://badge.fury.io/py/pymarktex.svg)](https://badge.fury.io/py/pymarktex)

# `pymarktex` version 1.4.6

This program creates a PDF file out of a specifically formated markdown text file.
In particular, the markdown file can contain extra information that
will be included in the final PDF with a fancy header. See the example included.

## Prerequisites

Since `pymarktex` is written in python, it is compatible with all operating systems: Linux, macOS and Windows. The main prerequisite is `python3` (which is often installed by default) along with the `pip3` package manager.

To check if you have `python3` installed, type the following on your terminal:

    $ python3 -V

If you do not have `python3` installed, please refer to the section [obtaining python3](docs/installing_tips.md#obtaining-python3).

To check you have `pip3` installed, type the following on your terminal:

    $ pip3 -V

If you do not have `pip3` installed, please refer to the section [obtaining pip3](docs/installing_tips.md#obtaining-pip3).

## Dependencies

The `pymarktex` package requires two other external tools to function. These are `pandoc` and `xelatex`

### Obtaining pandoc

Pandoc is a text conversion engine. The `pandoc` executable should be in your `$PATH`. To install it on a recent Ubuntu distribution simply type:

    $ sudo apt-get update
    $ sudo apt-get install pandoc
    
### Obtaining xelatex

This is type setting engine that creates PDF output. The `xelatex` executable should be in your `$PATH`.

To install it on a recent Ubuntu distribution simply type:

    $ sudo apt-get update
    $ sudo apt-get install texlive-full

Otherwise if that does not work, you can use the installer from the TeX Live package:

    $ wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    $ tar xzf install-tl-unx.tar.gz
    $ cd install-tl-*
    $ ./install-tl -gui text

## Installing

To install the `pymarktex` package, simply type the following commands on your terminal:

    $ pip3 install --user pymarktex

Alternatively, if you want to install it for all users of the system:

    $ sudo pip3 install pymarktex

## Usage

You can use it from the shell like this:

    $ pymarktex lorem.md

And it will generate the corresponding `lorem.pdf` file in the same directory.

## Extra documentation 

More documentation is available at:

<http://xapple.github.io/pymarktex/pymarktex>

This documentation is simply generated with:

    $ pdoc --html --output-dir docs --force pymarktex