#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    shuffle.py: Various ways to shuffle an array of elements
"""

__date__ = "09/06/2011"
__version__ = "0.3"

try:
    import csv
    import os
    import random  # You only needs this module for algorithms
    import sys
    from itertools import permutations
    from math import sqrt
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


try:
    import matplotlib.pyplot as plt
    from matplotlib.figure import SubplotParams
    NO_GRAPHS = False
except ImportError:
    NO_GRAPHS = True


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

    def faulty(lst):
        "An example of a intuitive but very bad algorithm."
        lst_length = len(lst)
        for i in range(lst_length):
            j = random.randrange(lst_length)
            lst[i], lst[j] = lst[j], lst[i]

    # The functions to test and the dictionary where store the results for each
    # possible permutation
    defs = [fisher_yates, knuth_durstenfeld, faulty]
    stats = {"".join([str(ch) for ch in pm]): {func.__name__: 0 for func in defs}
             for pm in permutations(array)}

    # Do the test. Always starting from the same array. Cause shuffle functions
    # are in-place operations, use str() & eval() to not alter the results.
    array = str(array)
    for func in defs:
        for i in range(iterations):
            lst = eval(array)
            func(lst)
            stats["".join([str(e) for e in lst])][func.__name__] += 1

    num_prm = len(stats)  # number of permutations
    ideal = iterations / num_prm
    mean = ((iterations / float(num_prm)) * 100) / iterations

    # Prepare the graphs
    splot_pars = SubplotParams(wspace=0.4, left=0.08, right=0.97, top=0.92)
    plt.figure(1, figsize=(6, 5), subplotpars=splot_pars)

    # Let's prepare the results for presentation
    for idx, fnc in enumerate([f.__name__ for f in defs], 1):
        deviations = []
        biases = []

        ## Store test results in a csv file and print to screen
        csvf = csv.writer(open("shuffle_{0}.csv".format(fnc), "w"))
        csvf.writerow(["Algorithm", fnc.replace("_", "-").title()])
        csvf.writerow(["Initial Array", array])
        csvf.writerow(["Iterations", iterations])
        csvf.writerow(["Ideal number of times", ideal])
        csvf.writerow([])
        csvf.writerow(["Permutation", "Times", "Bias", "Percent", "Deviation"])
        print(fnc.title().replace("_", "-").center(50))
        print(("=" * (len(fnc) + 2)).center(50) + os.linesep)
        print(" Permutation    Times     Bias    Percent   Deviation")
        print("------------- --------- -------- --------- -----------")

        for permu in sorted(stats):
            # do the calcs
            times = stats[permu][fnc]
            bias = times - ideal
            biases.append(bias)
            percent = (times * 100.0) / iterations
            deviation = percent - mean
            deviations.append(abs(deviation))

            csvf.writerow([permu, times, bias, str(percent).replace(".", ","),
                          str(deviation).replace(".", ",")])
            print("{0:10} {1:10} {2:10} {3:9.2f} {4:11.3f}".
                  format(permu, times, bias, percent, deviation))

        # calculate the standard deviation
        std_deviation = sqrt(sum([pow(b, 2) for b in biases]) / len(biases))

        # calculate mean deviation
        mean_deviation = sum(deviations) / len(deviations)

        csvf.writerow([])
        csvf.writerow(["Standard Deviation", "", "", "",
                       str(std_deviation).replace(".", ",")])
        csvf.writerow([])
        csvf.writerow(["Mean Deviation", "", "", "",
                       str(mean_deviation).replace(".", ",")])

        print(os.linesep + 'Standard deviation:'.center(50))
        print('{0:.3f}'.format(std_deviation).center(50))

        print(os.linesep + 'Mean deviation:'.center(50))
        print('\302\261{0:.3f}%'.format(mean_deviation).center(50) +
                                        os.linesep)

        # Plot the bar graphs
        plt.subplot(int("1{0}{1}".format(len(defs), idx)))
        values = ([stats[p][fnc] - ideal for p in sorted(stats, reverse=True)])
        plt.barh(range(1, num_prm + 1), values, 0.65, align="center",
                 label=fnc, color={1: "#CAF3C8", 2: "#C3D4FD",
                                   3: "#FACEC8"}.get(idx, "y"))
        plt.title(fnc.replace("_", " ").title(), color="#123A78", fontsize=14)
        plt.xlabel("bias")
        plt.grid(True, color="0.6")
        plt.yticks(range(1, num_prm + 1), [a for a in sorted(stats, reverse=1)],
                   family="monospace", weight="bold", fontsize=10)
        xlbls = [i / 2 for i in range(-ideal, ideal + (ideal / 2), ideal / 2)]
        plt.xticks(xlbls, xlbls, fontsize=9, family="monospace")

    # Show and save the graphs
    plt.savefig("shuffle_algorithms")
    plt.show()


if __name__ == "__main__":
    main(24000, ['A', 'K', 'Q', 'J'])  # Number of iterations & Sample array
