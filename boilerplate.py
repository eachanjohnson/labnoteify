#!/usr/bin/env python

__author__ = 'Eachan Johnson'

"""
'\\033[95mCONCENSUS'\\033[0m
(c) 2015 Eachan Johnson

Software suite for dealing with Illumina sequencing barcode counting for multiplex growth assays.

This is the collection of strings used often throughout the suite.
"""

## Define functions
def welcome():
    import time
    import colorama
    colorama.init()
    welcome_text = '\n' \
                   'CONCENSUS\n' \
                   '(c) 2015 Eachan Johnson\n\n' \
                   'The date is {} and the time is {}.\n' \
                   '\n'.format(
        time.strftime('%A, %Y-%m-%d'),  # Date
        time.strftime('%-I:%M %p')      # Time
    )
    return colorama.Fore.BLUE + welcome_text + colorama.Fore.RESET

def goodbye():
    import random  # For getting random numbers
    import colorama
    random_number = random.random()
    random_integer = int(random_number * (len(random_quotes)))
    random_quote = random_quotes[random_integer]  # Choose a random quotation to close with
    goodbye_text = '\n' \
                   'Done!\n\n' \
                   '{}\n' \
                   '\n'.format(random_quote)
    return colorama.Fore.GREEN + goodbye_text + colorama.Fore.RESET

def misuse_warning():
    import colorama
    warning = colorama.Fore.RED + '\nYou\'re doing it wrong!\nTry \'cnzs help\' (without quotes).\n' + \
              colorama.Fore.RESET
    return warning

## Define global variables
random_quotes = [
    '"Equipped with his five senses, man explores the universe around him and calls the adventure Science."\n'
    '\tEdwin Powell Hubble, The Nature of Science, 1954',
    '"I think science has enjoyed an extraordinary success because it has such a limited and narrow realm in which to '
    'focus its efforts. Namely, the physical universe."\n'
    '\tKen Jenkins',
    '"No one should approach the temple of science with the soul of a money changer."\n'
    '\tThomas Browne',
    '"If you\'re not part of the solution, you\'re part of the precipitate."\n'
    '\tHenry J. Tillman',
    '"Nature composes some of her loveliest poems for the microscope and the telescope."\n'
    '\tTheodore Roszak, Where the Wasteland Ends, 1972',
    '"There is something fascinating about science. One gets such wholesale returns of conjecture out of such a trifling'
    ' investment of fact."\n'
    '\tMark Twain, Life on the Mississippi, 1883'
]


## Boilerplate
if __name__ == '__main__':
    print(misuse_warning())