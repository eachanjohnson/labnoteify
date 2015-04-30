#!/usr/bin/env python

__author__ = 'Eachan Johnson'

__doc__ = """
Usage:  labnoteify noteify (-h|--help)
        labnoteify noteify --version
        labnoteify noteify [-v|--verbose] [-q|--quiet]

Options:
    -h, --help      Show this page and exit
    --version       Show version and exit
    -v, --verbose   Be more verbose. Over-rides --quiet/-q
    -q, --quiet     Be more quiet
"""

## Define functions
def find_files(root, ignore):
    import os
    file_list = []
    print 'Finding files in ', root
    walker = os.walk(root)
    for dir, subdirs, filenames in walker:
        file_list += [os.path.join(dir, filename) for filename in filenames]

    cleaned_file_list = []
    #file_list_gen = (name for name in file_list)
    for filename in file_list:
        if '/Volumes/' in filename:
            print filename
        do_i_ignore = False
        for ign_dir in ignore['dir']:
            test = ign_dir[:-1]
            if test in filename:
                do_i_ignore = True
            #print 'dir', test, filename, do_i_ignore
        if not do_i_ignore:
            test = filename.split('/')[-1]
            if test.split('.')[-1] in ignore['ext'] and test[0] != '.':
                do_i_ignore = False
            else:
                do_i_ignore = True
            #print 'ext', ign_ext, test.split('.')[-1] == ign_ext, test[0] != '.', filename, do_i_ignore
        if not do_i_ignore:
            cleaned_file_list.append(filename)
            #print 'Adding to notebook: ', filename
        else:
            pass
            #print 'Ignoring: ', filename
    return cleaned_file_list


def main():
    import docopt       # For super-smart command line option parsing
    #import subprocess   # For making bash calls
    import toolkit
    import json

    args = docopt.docopt(__doc__, version='Labnoteify 0.01')  # Parse command line arguments
    #print args

    setup = json.load(open('noteify.config', 'rU'))
    #print setup

    file_names = find_files(root=setup['root'], ignore=setup['ignore'])

    file_list = []
    for path in file_names:
        try:
            file_list.append(toolkit.LabnotiFile(path=path, root=setup['root'], type=path.split('.')[-1]))
        except OSError:
            pass
    #print file_list[0]

    file_list = sorted(file_list, key=lambda x: x.epoch_date)
    dates = list(set([f.date for f in file_list if f.size < 1000000]))
    day_list = []
    for date in dates:
        day_list.append(toolkit.Day([f for f in file_list if f.date == date and f.size < 1000000]))
    nb = toolkit.Notebook(day_list=day_list)
    toolkit.html_gen(notebook=nb, outdir=setup['output'])
    return None

## Boilerplate
if __name__ == '__main__':
    main()