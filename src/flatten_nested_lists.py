#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    flatten_nested_lists.py: Various ways to flatten a nested list.
"""

__date__ = "22/12/2010"
__version__ = "0.1"

try:
    import sys
    import os
    import collections
    import itertools
except ImportError:
    # Checks the installation of the necessary python modules 
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)

#---------------------------------------------------------- For All Nested lists

# The best way
def flatten(lst):
    """Flatten a nested list."""
    for elem in lst:
        if (isinstance(elem, collections.Iterable) and
            not isinstance(elem, basestring)):
            for sub in flatten(elem):
                yield sub
        else:
            yield elem

# Another way
def flatten_tl(lst):
    """Flatten a nested list of tuples/lists."""
    for elem in lst:
        if type(elem) in (tuple, list):
            for i in flatten(elem):
                yield i
        else:
            yield elem

# poor way. Worse memory consumption and worse performance
def flatten_list(lst):
    """Flatten a nested list without using generators."""
    result = []
    for elem in lst:
        if hasattr(elem, "__iter__") and not isinstance(elem, basestring):
            result.extend(flatten(elem))
        else:
            result.append(elem)
    return result


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
    "A one-liner list of lists"
    return sum(lst, [])


def main():
    """Main section"""

    nested_list = [1, 2, ['a', 'b', 'c'], 3, ['A', ('AA', 'AB', ['AAA'])], 4]
    list_of_iterables = [(1, 2), ['a', 'b'], ['A', 'B', ('AA', ['AAA'])]]
    list_of_lists = [[1, 2], ['a', 'b'], ['A', 'B', ['AA']]]

    print('All Nested lists'.center(80))
    print(('"' * 18).center(80) + os.linesep)
    print('Sample list:       {0}'.format(nested_list) + os.linesep)
    print('flatten:           {0}'.format([i for i in flatten(nested_list)]))
    print('flatten_tl:        {0}'.format([i for i in flatten_tl(nested_list)]))
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
