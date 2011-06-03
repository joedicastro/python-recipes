#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    flatten_nested_lists.py: Various ways to flatten a nested list.
"""

__date__ = "4/06/2011"
__version__ = "0.4"

try:
    import csv
    import os
    import itertools
    import random
    import sqlite3
    import sys
    import timeit
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


#---------------------------------------------------------- For All Nested lists

# Best way, Best performance. Not recursive.
# By Chema Cortes (http://Ch3m4.org) at http://python.majibu.org/preguntas/547/
def flat_slice(lst):
    """Flatten a nested list using the slice operation."""
    lst = list(lst)
    for i, _ in enumerate(lst):
        while (hasattr(lst[i], "__iter__") and not
               isinstance(lst[i], basestring)):
            lst[i:i + 1] = lst[i]
    return lst

# Seen at http://kogs-www.informatik.uni-hamburg.de/~meine/python_tricks
# Good performance, but recursive (initial python recursion limit = 1K levels)
def flat_list(lst):
    """Flatten a nested list without using generators."""
    result = []
    for elem in lst:
        if hasattr(elem, "__iter__") and not isinstance(elem, basestring):
            result.extend(flat_list(elem))
        else:
            result.append(elem)
    return result

# By Ch3m4 Cortes (http://Ch3m4.org) at http://python.majibu.org/preguntas/547/
# Poor performance.
def flat_sum(lst):
    """Flatten a nested list using the sum function."""
    return sum((flat_sum(elem) if
                hasattr(elem, "__iter__") and not isinstance(elem, basestring)
                else [elem] for elem in lst), [])

# Seen at http://stackoverflow.com/questions/2158395#2158532
# Poor performance.
#
# You can replace this line
#
# if hasattr(elem, "__iter__") and not isinstance(elem, basestring):
#
# by this:
#
# if (isinstance(elem, collections.Iterable) and
#     not isinstance(elem, basestring)):
#
# or by this (only for a nested list of tuples/lists):
#
# if type(elem) in (tuple, list)
#
# With similar results and almost same performance.
def flat_yield(lst):
    """Flatten a nested list."""
    def flatten(lst):
        """Do the real job"""
        for elm in lst:
            if hasattr(elm, "__iter__") and not isinstance(elm, basestring):
                for sub in flatten(elm):
                    yield sub
            else:
                yield elm
    return list(flatten(lst))

#---------------------------------------- For one level Nested list of iterables

## Working only in a one level nesting ##

# Best & fastest way
def flatten_one_liner(lst):
    """A one-liner nested lists flattener."""
    return list(itertools.chain.from_iterable(lst))

# No needs import extra modules
def flattener(lst):
    """A one-liner nested lists flattener."""
    return [item for sublist in lst for item in sublist]


#------------------------------------------------------------- For list of lists

# Only for a one level list of lists
def flattener_sum(lst):
    "A one-liner only for a list of lists"
    return sum(lst, [])

#....................................................... A nested list generator

# This function generates nested lists, with the desired number of elements and
# levels of nesting. It's composed of integers and strings or only integers.
# It's intended to generate a regular structure, whatever the number of elements
# or levels. The intention is that when measuring performance, you get regular
# results in order to measure with precision the variation in performance
# depending on the number of elements and / or levels. This structure is like a
# list of nested lists, as a metaphor in the real world would be a field of
# ziggurats (stone step pyramids), hence its name. As an option you can create
# lists that contain generators to test that functions are not capable of
# handling these items.

def ziggurat(stones=1, steps=1, with_iters=False, only_numbers=False):
    """Make a list of nested lists, like a field of ziggurats."""
    # First, generate the list of the stones (numbers and "strings")
    as_str = [] if only_numbers else random.sample(range(stones), stones / 2)
    stones_list = [str(stn) if stn in as_str else stn for stn in range(stones)]
    # Find the number of step pyramids (aka ziggurats)
    num_zggts = stones / (steps + (steps - 1))
    ziggurats = []
    for zggt in range(num_zggts):
        zggt_step = []
        # Build a step pyramid, step by step, until the chosen level
        for step in range(steps):
            # Get a choice of stones from the list to make a step & remove them
            choice = random.sample(stones_list, 1 if not step else 2)
            for choosen in choice:
                stones_list.remove(choosen)
            # Build a step
            if not step:
                zggt_step.append(choice[0])
            else:
                choice.insert(1, iter(zggt_step) if with_iters else zggt_step)
                zggt_step = choice
        ziggurats.append(zggt_step)
    # IF don't have stones enough to make even a ziggurat, then will make
    # multiple one-stone-many-airsteps ziggurats
    if not num_zggts:
        for step in range(steps):
            for stn in range(0, stones, 2):
                stones_list[stn] = stones_list[stn:stn + 1]
    # Finally, mix the remaining stones and the ziggurats, et Voila!!!
    stones_list += ziggurats
    random.shuffle(stones_list)
    return stones_list


def main():
    """Main section. This is an example of how these methods work."""

    nested_list = [1, 2, ['a', 'b', 'c'], 3, ['A', ('AA', 'AB', ['AAA'])], 4]
    list_of_iterables = [(1, 2), ['a', 'b'], ['A', 'B', ('AA', ['AAA'])]]
    list_of_lists = [[1, 2], ['a', 'b'], ['A', 'B', ['AA']]]

    print('All Nested lists'.center(80))
    print(('"' * 18).center(80) + os.linesep)
    print('Sample list:       {0}'.format(nested_list) + os.linesep)
    print('flat_slice:        {0}'.format([z for z in flat_slice(nested_list)]))
    print('flat_sum:          {0}'.format([z for z in flat_sum(nested_list)]))
    print('flat_list:         {0}'.format([z for z in flat_list(nested_list)]))
    print('flat_yield:        {0}'.format([z for z in flat_yield(nested_list)]))
    print('')
    print('Nested lists of iterables'.center(80))
    print(('"' * 27).center(80) + os.linesep)
    print('List of iterables: {0}'.format(list_of_iterables) + os.linesep)
    print('flatten_one_liner: {0}'.format(flatten_one_liner(list_of_iterables)))
    print('flattener:         {0}'.format(flattener(list_of_iterables)))
    print('')
    print('Lists of lists'.center(80))
    print(('"' * 16).center(80) + os.linesep)
    print('List of lists:      {0}'.format(list_of_lists) + os.linesep)
    print('flattener_sum:      {0}'.format(flattener_sum(list_of_lists)))


if __name__ == "__main__":
    main()

    ### In this part will run performance tests for the first methods shown up
    ### If matplotlib is installed, plot and show the test GRAPHS, however the
    ### test results are stored in csv files.

    # The functions to test and the needed setup for timeit.
    DEFS = [f.__name__ for f in (flat_slice, flat_list, flat_sum, flat_yield)]
    SETUP = "from __main__ import nlst,{0}".format(",".join([d for d in DEFS]))

    # Create a sqlite database in memory to store the results
    CONN = sqlite3.connect(":memory:")
    CUR = CONN.cursor()
    CUR.execute("""create table results
                (graph text, def text, num int, lvl int, time real)""")

    # Define the values needed for each test (cases and graphs paramaters)
    GRAPHS = [(0, u"elements ↑ | = levels",
               [(n, 10) for n in range(20, 1410, 10)], 311),
              (1, u"elements = | ↑ levels",
               [(10, n) for n in range(10, 1610, 10)], 312),
              (2, u"elements ↑ | ↑ levels",
               [(n * 2 , n) for n in range(10, 1610, 10)], 313)]

    # Prepare the plot
    if not NO_GRAPHS:
        SPLOT_PARS = SubplotParams(hspace=0.5, left=0.10, right=0.96)
        FIG = plt.figure(1, figsize=(6.5, 8.8), subplotpars=SPLOT_PARS)

    # Do the performance tests for each graph. 10 iterations x function & case.
    for idx, graph, cases, pos in GRAPHS:
        for n, l in cases:
            with_iterables = False
            if not with_iterables:
                nlst = ziggurat(n, l, with_iterables)
            for f in DEFS:
                # I know, is not the same list for all the functions, but it
                # is the problem with iterables, they are single use only. 
                # Anyway the list structure is the same, just change the 
                # elements. So do not alter the results, only slows the test 
                # process.
                if with_iterables:
                    nlst = ziggurat(n, l, with_iterables)
                try:
                    tim = timeit.timeit("%s(nlst)" % f, SETUP, number=10)
                    CUR.execute("insert into results values (?, ?, ?, ?, ?)",
                                (graph, f, n, l, tim * 1e2))
                except:
                    # Uncomment only for debugging. It Normally Fail when reach 
                    # Python recursion limit (1K levels)
                    #print("{0} error: {1}".format(f, str(sys.exc_info()[1])))
                    CUR.execute("insert into results values (?, ?, ?, ?, ?)",
                                (graph, f, n, l, None))

        # Create the graphs
        if not NO_GRAPHS:
            ax = plt.subplot(pos)
            for fn, cl in (zip(DEFS, ['y', 'r', 'g', 'b'])):
                CUR.execute("""SELECT num, lvl, time FROM results WHERE def=?
                            and graph=?""", (fn, graph))
                values = CUR.fetchall()
                xs = [x[1] for x in values] if idx else [x[0] for x in values]
                ys = [y[2] for y in values]
                plt.plot(xs, ys, linewidth="1.5", color=cl, label=fn)
            plt.title(graph)
            plt.ylabel("time (ms)")
            plt.xlabel("elements" if not idx else "levels")
            plt.grid(True)

        ## Store test results in a csv file
        results = csv.writer(open("test_results_{0}.csv".format(idx), "w"))
        results.writerow(["elements", "levels"] + (DEFS))
        for cnum, clvl in cases:
            CUR.execute("""SELECT time FROM results WHERE graph=? and
                        num=? and lvl=?""", (graph, cnum, clvl))
            row = ([str(r[0]).replace(".", ",") for r in CUR.fetchall()])
            results.writerow([cnum, clvl, row[0], row[1], row[2], row[3]])

    # Show graphs and save them to a image file
    if not NO_GRAPHS:
        HANDLES, LABELS = ax.get_legend_handles_labels()
        FIG.legend(HANDLES, LABELS, loc=8, ncol=4, columnspacing=0.35)
        FIG.suptitle("Performance tests (flatten lists functions)", fontsize=17)
        plt.savefig("test_results")
        plt.show()
