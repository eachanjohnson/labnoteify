#!/usr/bin/env python

__author__ = 'Eachan Johnson'

__doc__ = """
Usage: cnzs [--version] [--help|-h] <command> [<args>...]

Options:
   -h, --help   Show this page and exit
   --version    Show version number and exit

The most commonly used cnzs commands are:
   setup        Install helper programs, like R
   map          Count and map FASTQ file reads to plates, strains, and compounds
   rearray      Re-array strain coutns to different wells
   remap        Re-annotate updated map data
   plot         Analyze and plot mapped sequencing data
   homology     Get known targets of hits
   chemlearn    Machine learning on screen data
See 'cnzs help <command>' for more information on a specific command.
"""

## Define functions
def main():
    import docopt       # For super-smart command line option parsing
    import boilerplate  # For grabbing reusable text
    import subprocess   # For making bash calls

    args = docopt.docopt(__doc__, version='CONCENSUS version 0.11', options_first=True)  # Parse command line arguments

    print(boilerplate.welcome())  # Say hello to the user

    argv = [args['<command>']] + args['<args>']
    if args['<command>'] in ['help', None]:
        try:
            subprocess.call(['python', 'cnzs_{}.py'.format(args['<args>'][0]), '--help'])
        except IndexError:
            subprocess.call(['python', 'cnzs.py', '--help'])
    elif args['<command>'] in ['setup', 'map', 'rearray', 'remap', 'plot', 'homology', 'chemlearn']:
        subprocess.call(['python', 'cnzs_{}.py'.format(args['<command>'])] + argv)
    else:
        print('{} is not a cnzs.py command. See \'cnzs help\'.\n'.format(args['<command>']))

    print(boilerplate.goodbye())  # Say goodbye to the user

    return None

## Boilerplate
if __name__ == '__main__':
    main()