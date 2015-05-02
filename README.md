# Labnoteify

Is your lab notebook made up of random files on your computer?

**Labnoteify** is a framework for compiling these into something more meaningful. After running `python labnoteify.py setup`, run `python labnoteify.py noteify` to convert everything you want into a browsable HTML notebook.

## Features
* Runs on Python 2.7, so portable for Unix, Mac OSX, Windows, Linux
* Organises most common files into a date-ordered HTML lab notebook:
    * R and Python code
    * XLSX spreadsheets (except embedded charts)
    * DOCX documents
    * PDFs
    * PNGs and JPEGs

## Wishlist
* PDF output for printing
* Compatibility with DOC and XLS legacy formats
* Use Markdown files to optionally embed narrative, override dates, and structure pages
* Prettier HTML

## Issues
* PDFs don't embed properly
* Not a `setup.py` installable package yet

## Requirements
* Python 2.7
* Python packages (all are available by `pip install`):
    * Wand
    * docopt
    * xlrd
* Ability to `cd` in the Terminal

## Usage
1. Download the files in this repository to a convenient location.
2. In the Terminal, `cd` to the directory containing these files.
3. Try `python labnoteify.py help` if you get stuck.
4. Run `python labnoteify.py setup`, follow the interactive instructions.
5. Run `python labnoteify.py noteify`, sit back and relax.
6. PDF conversion generates a lot of PNGs. You can delete them with `python labnoteify.py cleanup`, but leaving them will make re-compiling your notebook faster.

