#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    test_dir_tree.py: Make a fake dir hierarchy with files for test purposes
"""

#===============================================================================
# This Script makes a fake dir hierarchy with files for test purposes
#
# Uses the Lorem-Ipsum-Generator project by James Hales <jhales.perth@gmail.com>
# at http://code.google.com/p/lorem-ipsum-generator/
#===============================================================================

#===============================================================================
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
#
#===============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "24/10/2010"
__version__ = "0.1"

try:
    import sys
    import os
    import lipsum
    from random import randint, randrange, choice
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def test_tree(path, min_dirs=7, max_dirs=79):
    """make a fake directory hierarchy with files for test purposes."""

    def latin_words(generator):
        """Generate a list of latin words"""
        words = generator.generate_paragraphs_plain(9).lower()
        return list(set(words.replace('.', '').replace(',', '').split()))

    def check_path(path):
        """If no exists a path, make it."""
        if not os.path.exists(path):
            os.mkdir(path)

    lorem = lipsum.MarkupGenerator()
    latins = latin_words(lorem)

    dirs = latins[:randrange(min_dirs, max_dirs)]
    files = [f for f in latins if f not in dirs][:len((dirs) * 3) - 3]

    check_path(path)
    for directory in dirs:
        check_path(os.path.join(path, directory))

    for fil in files:
        filename = os.path.join(path, choice(dirs), '{0}.txt'.format(fil))
        text = ''
        size = randint(3, 524288) # Files not bigger than 512 Kbytes
        sample = lorem.generate_paragraphs_plain(randrange(3, 9))
        while len(text) < size:
            text += sample + os.linesep * 2
        with open(filename, 'w') as out:
            out.write(text[:size])

    return dirs, files

def main():
    """Main section"""

    # Create a test dir hierarchy
    path = './test/'
    folders, archives = test_tree(path)
    print '{0} folders & {1} files created'.format(len(folders), len(archives))


if __name__ == "__main__":
    main()
