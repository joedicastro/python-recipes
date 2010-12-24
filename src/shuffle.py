#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    shuffle.py: Various ways to shuffle an array of elements
"""

__date__ = "24/12/2010"
__version__ = "0.1"

try:
    import sys
    import os
    import random # You only needs this module for algorithms
    from re import sub
    from itertools import permutations
    from math import factorial
except ImportError:
    # Checks the installation of the necessary python modules 
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


# The original algorithm (1938) by Ronald Fisher and Frank Yates, implemented 
# in Python
def fisher_yates(lst):
    "Python implementation of the original Fisher-Yates algorithm."
    if len(lst) > 1:
        idx = len(lst) - 1
        while idx > 0:
            sel = random.randint(0, idx)
            lst[idx], lst[sel] = lst[sel], lst[idx]
            idx -= 1

# The Richard Durstenfeld's version (1964) popularized by Donald Knuth in 
# volume 2 of his book The Art of Computer Programming as "Algorithm P", 
# Implemented in Python 

## Is the same of shuffle() in Python standard module random. Then use 
## random.shuffle() instead.
def knuth_durstenfeld(lst):
    "Python implementation of the Durstenfeld algorithm popularized by Knuth."
    for idx in reversed(range(1, len(lst))):
        # pick an element in lst[:idx+1] with which to exchange lst[idx]
        sel = random.randrange(idx + 1)
        lst[idx], lst[sel] = lst[sel], lst[idx]


# Original by Sandra Sattolo in 1986. This only cycle the position of the 
# elements in the array. In Python too.
def sattolo_cycle(lst):
    "Python implementation of the original Sattolo Cycle algorithm."
    idx = len(lst)
    while idx > 1:
        idx = idx - 1
        sel = random.randrange(idx)  # 0 <= sel <= idx-1
        lst[sel], lst[idx] = lst[idx], lst[sel]
    return


def main(iterations, array):
    """An example of these algorithms"""

    def definitions():
        """Reset the variables for each algorithm"""
        # All possible combinations as string in a dictionary with a counter of 
        # apparitions reset to 0
        combos = dict(zip((sub("[^\d ]", "", (str(i)))
                           for i in permutations(array)),
                           [0 for i in range(factorial(len(array)))]))
        mean = ((iterations / len(combos)) * 100.0) / iterations
        return array, combos, mean, []

    for algorithm in [fisher_yates, knuth_durstenfeld, sattolo_cycle]:
        lst, combos, mean, deviations = definitions()
        for iter in range(iterations):
            algorithm(lst)
            combos[sub("[^\d ]", "", str(lst))] += 1

        # print the header for each algorithm
        print(algorithm.__name__.title().replace("_", "-").center(38))
        print(("=" * (len(algorithm.__name__) + 2)).center(38) + os.linesep)
        print(" " * ((len(lst) * 2) - 6) + "Combo  Appears  Percent  Deviation")
        print(" " * ((len(lst) * 2) - 6) + "-----  -------  -------  ---------")

        for combo in sorted(combos):
            percent = (combos[combo] * 100.0) / iterations
            deviation = percent - mean
            deviations.append(abs(deviation))
            # print the combinations and his apparitions, percentage of total 
            # and deviation from mean
            print("{0}  {1:7}{2:8.2f}%{3:10.3f}%".format(combo, combos[combo],
                                                         percent, deviation))

        mean_deviation = sum(deviations) / len(deviations)
        # Print the mean deviation of each algorithm
        print(os.linesep + 'Mean deviation:'.center(38))
        print('\302\261{0:.3f}%'.format(mean_deviation).center(38) + os.linesep)


if __name__ == "__main__":
    main(60000, [1, 2, 3]) # Number of iterations & Sample numeric array
