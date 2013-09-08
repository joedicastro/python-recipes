#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    web_lxml.py: Reads a webpage with lxml and prints its element tree.
"""

#==============================================================================
# Reads a webpage with lxml and prints its element tree. Prints the structure
# of the object element, which is a list of lists, a tree structure. We use it
# to locate those elements you want to parse to extract the necessary data.
#==============================================================================

#==============================================================================
#    Copyright 2010 joe di castro <joe@joedicastro.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#==============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "26/12/2010"
__version__ = "0.1"

try:
    import sys
    import os
    import urllib2
    import lxml.html
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def read_web(url):
    """Read a HTML web page, parses it and converts to a lxml element."""
    element = lxml.html.fromstring(urllib2.urlopen(url).read())
    return element


def print_tree(branch, idx=""):
    """Prints the structure of the object element, which is a list of lists, a
    tree structure. We use it to locate those elements you want to parse to
    extract the necessary data"""
    if not branch.getchildren():
        print("{0} - {1} - {2}{3}".format(idx, branch.tag, branch.text,
                                          os.linesep))
    else:
        print("{0} - {1} - {2}{3}".format(idx, branch.tag, branch.text,
                                          os.linesep))
        for subtree in xrange(0, len(branch)):
            print_tree(branch[subtree], ("{0}[{1}]".format(idx, subtree)))


def main():
    """Main section"""

    print_tree(read_web("http://google.com"))

if __name__ == "__main__":
    main()
