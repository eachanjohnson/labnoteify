#!/usr/bin/env python

__author__ = 'Eachan Johnson'

__doc__ = """
Usage:  labnoteify cleanup (-h|--help)
        labnoteify cleanup --version
        labnoteify cleanup [-v|--verbose] [-q|--quiet]

Options:
    -h, --help      Show this page and exit
    --version       Show version and exit
    -v, --verbose   Be more verbose. Over-rides --quiet/-q
    -q, --quiet     Be more quiet
"""

## Define functions
def main():
    import docopt       # For super-smart command line option parsing
    import json
    import labnoteify_noteify
    import os

    args = docopt.docopt(__doc__, version='Labnoteify 0.01')  # Parse command line arguments
    #print args

    setup = json.load(open('noteify.config', 'rU'))
    #print setup

    file_names = labnoteify_noteify.find_files(root=setup['root'], ignore=setup['ignore'])

    files_to_delete = set()
    print 'Cleaning up stray labnoteify PNGs'
    for n, path in enumerate(file_names):
        #print n
        filename = path.split('/')[-1]
        filename_root = path.split('/')[-1][:-4]
        ext = filename[-4:]
        path_name = path.split(filename)[0]
        #print path, filename, filename_root, ext, path_name, filename_root + '.pdf' in os.listdir(path_name)
        try:
            if ext == '.pdf':
                png_list = [f for f in os.listdir(path_name) if f[-12:] == '.noteify.png' and filename_root in f]
                for png in png_list:
                    png_path = path_name + png
                    print 'Primed to delete', png_path
                    files_to_delete.add(png_path)
        except OSError:
            pass
    #print file_list[0]

    # Delete files
    if len(files_to_delete) > 0:
        do_i_delete = raw_input('Do you want me to delete {} files? [yes/no]\n'.format(len(files_to_delete)))
        if do_i_delete == 'yes':
            for path in files_to_delete:
                try:
                    os.remove(path)
                except Exception as e:
                    print e
        else:
            pass
    else:
        print('Nothing to delete!')
    return None

## Boilerplate
if __name__ == '__main__':
    main()