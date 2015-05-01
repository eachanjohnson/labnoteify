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

    root = raw_input('What is the root directory to drill down for notebook content?\n')

    output = raw_input('In which directory do you want me publish your notebook? '
                       'If it doesn\'t exist, I\'ll create it.\n')

    ignore_list = raw_input('Please give me the path to a text file listing the extensions of file types you want to '
                            'include and the paths (relative to the directory above) you want to ignore.\n')

    try:
        ignore_list = open(ignore_list, 'rU').read().split('\n')[:-1]
    except IOError:
        ignore_list = ignore_list.split(' ')

    noteify_ignore = {
        'ext': [item[1:] for item in ignore_list if item[0] == '.' and len(item) != 0],
        'dir': ['{}/{}'.format(root, item) for item in ignore_list if item[-1:] == '/']
    }

    setup = {'root': root, 'output': output, 'ignore': noteify_ignore}
    return setup

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
    print answers
    write_config_file(filename='noteify.config', answers=answers)

    return None

## Boilerplate
if __name__ == '__main__':
    main()