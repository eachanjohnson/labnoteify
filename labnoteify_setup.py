#!/usr/bin/env python

__author__ = 'Eachan Johnson'

__doc__ = """
Usage: cnzs setup [-v|--verbose] [-q|--quiet] [-h|--help]

Options:
    -h, --help      Print this page and exit
    -v, --verbose   Be more verbose. Over-rides --quiet/-q
    -q, --quiet     Be more quiet
"""

## Define functions
def questionnnaire():
    print('Let me ask some questions.\n')

    directories = raw_input('Which directories do you want me to look in? Give the name of a TXT file with a list'
                           'of directories, or provide the top directory of a tree you want me to drill down.\n')

    noteify_ignore = raw_input('\nDo you want me to ignore any file types? Say no or give a space-separated list of '
                              'file extensions.\n')

    return {'dir': directories, 'ignore': noteify_ignore}

def write_config_file(filename, answers):
    import json
    with open(filename, 'w') as f:
        json.dump(answers, f)
    return filename

def main():
    import docopt       # For super-smart command line option parsing
    import subprocess   # For making bash calls

    args = docopt.docopt(__doc__)  # Parse command line arguments

    if args['--verbose']:
        verbosity = 2
    elif args['--quiet']:
        verbosity = 0
    else:
        verbosity = 1

    answers = questionnnaire()
    write_config_file(filename='noteify.config', answers=answers)

    return None

## Boilerplate
if __name__ == '__main__':
    main()