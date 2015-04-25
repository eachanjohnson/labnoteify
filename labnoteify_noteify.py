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
def main():
    import docopt       # For super-smart command line option parsing
    import subprocess   # For making bash calls

    args = docopt.docopt(__doc__)  # Parse command line arguments

    print('Seeing if you have R installed...')
    install_r = 'no'
    try:
        r_path = subprocess.check_output(['which', 'Rscript']).rstrip()
    except subprocess.CalledProcessError:
        install_r = raw_input('You don\'t have R installed. Do you want to install it? [yes/no]\n')
    else:
        print('R is installed, and located at {}.'.format(r_path))

    if install_r.lower() == 'yes' or install_r.lower() == 'y':
        import platform
        import urllib2
        system  = platform.system()
        url = False
        if system == 'Darwin':
            distro = system
            version = platform.mac_ver()[0]
            version_no = int(version.split('.')[1])
            if version_no >= 9:
                url = 'http://cran.rstudio.com/bin/macosx/R-3.1.3-snowleopard.pkg'
            elif version_no >= 6:
                url = 'http://cran.rstudio.com/bin/macosx/R-3.1.3-snowleopard.pkg'
            else:
                exit('Sorry! MacOS X version {} is unsupported. You can still use parts of CONCENSUS'.format(version))
        elif system == 'Linux':
            linux_info = platform.linux_distribution(full_distribution_name=False)
            distro = linux_info[0]
            version = linux_info[1]
            exit('Sorry! Go to http://cran.rstudio.org and download R for Linux {} {}. '
                 'Then run \'cnzs setup\' again'.format(distro, version))
        elif system == 'Windows':
            distro = system
            version = platform.win32_ver()[1]
            exit('Go to http://cran.rstudio.org and download R for Linux {} {}. Then run \'cnzs setup\' again'.format(
                distro, version
            ))
        else:
            exit('Sorry! Couldn\'t detect your system version to download R. Go to http://cran.rstudio.org.')
        if url:
            try:
                request = urllib2.urlopen(url)
                with open('R-download.pkg', 'w') as f:
                    f.write(request.read())
            except urllib2.HTTPError:
                exit('Sorry! Couldn\'t seem to download R for MacOS X version {}. '
                     'Go to http://cran.rstudio.org.'.format(version))
            else:
                print('Downloaded R from {}\n'
                      'You need to install it yourself.'.format(url))

    print('You should be all set.')
    return None

## Boilerplate
if __name__ == '__main__':
    main()