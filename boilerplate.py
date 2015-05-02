#!/usr/bin/env python

__author__ = 'Eachan Johnson'

## Define functions
def welcome():
    import time
    import colorama
    colorama.init()
    welcome_text = '\n' \
                   'Labnoteify\n' \
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
    warning = colorama.Fore.RED + '\nYou\'re doing it wrong!\nTry \'labnoteify help\' (without quotes).\n' + \
              colorama.Fore.RESET
    return warning

## Define global variables
random_quotes = [
    '"Equipped with his five senses, man explores the universe around him and calls the adventure Science."\n'
    '\t- Edwin Powell Hubble, The Nature of Science, 1954',
    '"I think science has enjoyed an extraordinary success because it has such a limited and narrow realm in which to '
    'focus its efforts. Namely, the physical universe."\n'
    '\t- Ken Jenkins',
    '"No one should approach the temple of science with the soul of a money changer."\n'
    '\tThomas Browne',
    '"If you\'re not part of the solution, you\'re part of the precipitate."\n'
    '\t- Henry J. Tillman',
    '"Nature composes some of her loveliest poems for the microscope and the telescope."\n'
    '\t- Theodore Roszak, Where the Wasteland Ends, 1972',
    '"There is something fascinating about science. One gets such wholesale returns of conjecture out of such a '
    'trifling investment of fact."\n'
    '\t- Mark Twain, Life on the Mississippi, 1883',
    '"It is strange that only extraordinary men make the discoveries, which later appear so easy and simple."\n'
    '\t- Georg C. Lichtenberg',
    '"Actually, everything that can be known has a Number; for it is impossible to grasp anything with the mind or to '
    'recognize it without this."\n'
    '\t- Philolaus',
    '"God created two acts of folly. First, He created the Universe in a Big Bang. Second, He was negligent enough to '
    'leave behind evidence for this act, in the form of microwave radiation."\n'
    '\t- Paul Erdos',
    '"Progress is made by trial and failure; the failures are generally a hundred times more numerous than the '
    'successes; yet they are usually left unchronicled."\n'
    '\t- William Ramsay',
    '"Although Nature needs thousands or millions of years to create a new species, man needs only a few dozen years to'
    ' destroy one."\n'
    '\t- Victor Scheffer',
    '"There may be babblers, wholly ignorant of mathematics, who dare to condemn my hypothesis, upon the authority of '
    'some part of the Bible twisted to suit their purpose. I value them not, and scorn their unfounded judgment."\n'
    '\t- Nicolaus Coperincus',
    '"If your experiment needs statistics, you ought to have done a better experiment."\n'
    '\t- Ernest Rutherford',
    '"By \'life\', we mean a thing that can nourish itself and grow and decay."\n'
    '\t- Aristotle',
    '"A physicist is an atom\'s way of knowing about atoms."\n'
    '\t- George Wald',
    '"An experiment is a question which science poses to Nature, and a measurement is the recording of Nature\'s answer."\n'
    '\t- Max Planck',
    '"A fact acquires its true and full value only through the idea which is developed from it."\n'
    '\t- Justus von Leibig',
    '"There is no law except the law that there is no law."\n'
    '\t- John Archibald Wheeler',
    '"Falsity in intellectual action is intellectual immorality."\n'
    '\t- Thomas Chrowder Chamberlain',
    '"Outstanding examples of genius - a Mozart, a Shakespeare, or a Carl Friedrich Gauss - are markers on the path '
    'along which our species appears destined to tread."\n'
    '\t- Fred Hoyle',
    '"Science is the acceptance of what works and the rejection of what does not. That needs more courage than we might think."\n'
    '\t- Jacob Bronkowski',
    '"I believe there are 15 747 724 136 275 002 577 605 653 961 181 555 468 044 717 914 527 116 709 366 231 425 076 '
    '185 631 031 296 protons in the universe and the same number of electrons."\n'
    '\t- Sir Arthur Eddington'

]


## Boilerplate
if __name__ == '__main__':
    print(misuse_warning())