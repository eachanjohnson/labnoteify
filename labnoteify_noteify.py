#!/usr/bin/env python

__author__ = 'Eachan Johnson'

__doc__ = """
Usage:  labnoteify noteify (-h|--help)
        labnoteify noteify --version
        labnoteify noteify [-v|--verbose] [-q|--quiet]
        labnoteify noteify (-c|--count)

Options:
    -h, --help      Show this page and exit
    --version       Show version and exit
    -v, --verbose   Be more verbose. Over-rides --quiet/-q
    -q, --quiet     Be more quiet
    -c, --count     Just count the number of files that would be included in the notebook
"""

## Define functions
def find_files(root, ignore, verbosity=0):
    import os
    file_list = []
    print 'Finding files in', root
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
    if verbosity > 0:
        print len(cleaned_file_list), 'files found.'
    return cleaned_file_list


def main():
    import docopt       # For super-smart command line option parsing
    import toolkit
    import json

    args = docopt.docopt(__doc__, version='Labnoteify 0.01')  # Parse command line arguments
    #print args

    setup = json.load(open('noteify.config', 'rU'))
    #print setup

    if args['--count']:
        verbosity = 0
    elif args['--verbose']:
        verbosity = 2
    elif args['--quiet']:
        verbosity = 0
    else:
        verbosity = 1

    file_names = find_files(root=setup['root'], ignore=setup['ignore'], verbosity=verbosity)
    if args['--count']:
        return '{} files found.'.format(len([f for f in file_names if '.noteify' not in f]))

    file_list = []
    len_file_names = len(file_names)
    print 'Converting files to HTML. This may take a while...'
    for n, path in enumerate(file_names):
        if verbosity > 1:
            if not '.noteify' in path and not '.png' in path:
                print 'HTMLifying file number {} of {}:'.format(n, len_file_names), path
            else:
                pass
        try:
            file_list.append(toolkit.LabnotiFile(path=path, root=setup['root'], type=path.split('.')[-1]))
        except OSError:
            pass
    #print file_list[0]

    file_list = sorted(file_list, key=lambda x: x.epoch_date)
    dates = list(set([f.date for f in file_list if f.html != '']))
    day_list = []
    for date in dates:
        day_list.append(toolkit.Day([f for f in file_list if f.date == date]))
    nb = toolkit.Notebook(day_list=day_list)
    toolkit.html_gen(notebook=nb, outdir=setup['output'])
    if verbosity > 0:
        return 'Wrote notebook in', setup['output']
    else:
        return ''

## Boilerplate
if __name__ == '__main__':
    try:
        print(main())
    except KeyboardInterrupt:
        print('Goodbye!')