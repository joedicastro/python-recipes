#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
    remove_duplicates.py: Remove duplicate files (filtered or not by extension)
"""

# =============================================================================
# This script find duplicate files by a given (or not) extension in a
# given path (or the current one) and delete them. Only a file of each
# set of duplicates is left intact, and this script not try by any way
# to discern which one is the original, it simply preserves the first
# one in chronological order.
# =============================================================================

# =============================================================================
#    Copyright 2015 joe di castro <joe@joedicastro.com>
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
# =============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "2015-08-19"
__version__ = "0.1"

try:
    import glob
    import hashlib
    import os
    import sys
    from argparse import ArgumentParser
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def arguments():
    """Defines the command line arguments for the script."""
    cur_dir = os.path.curdir
    main_desc = """Remove all duplicate files leaving only one copy."""
    usage = "%(prog)s [-p SRC] [-e EXT] [-t] [-vv] [--help]"

    parser = ArgumentParser(description=main_desc, usage=usage)
    parser.add_argument("-p", "--path", dest="path", default=cur_dir,
                        help="the path. Current dir if none is provided")
    parser.add_argument("-e", "--ext", dest="ext", default="*",
                        help="filter by file extension")
    parser.add_argument("-t", "--test", dest="test", action="store_true",
                        help="test the result without delete anything")
    parser.add_argument("-vv", "--verbose", dest="verbose",
                        action="store_true",
                        help="print the name of each deleted filename")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {0}".format(__version__),
                        help="show program's version number and exit")
    return parser


def remove_dup_files(args, count=0):
    """Remove duplicate files in a directory."""
    os.chdir(args.path)
    filtered = glob.glob("*.{0}".format(args.ext))
    unique, total = set(), len(filtered)

    # Even when MD5 is fundamentally broken for cryptographic uses, in
    # this particular case the risk of a collision is minimal and the
    # performance is good enough, specially compared with other more
    # accurate algorithms. Despite that, the risk of a collision
    # exists, thus use it with caution!
    files = {
        i: {
            "time": os.stat(i).st_ctime,
            "path": os.path.join(args.path, i),
            "hash": hashlib.md5(open(i).read()).hexdigest()
        } for i in filtered
    }

    for i in sorted(files, key=lambda x: files[x]["time"]):
        if files[i]["hash"] in unique:
            os.remove(files[i]["path"]) if not args.test else None
            if args.verbose:
                print(files[i]["path"])
            count += 1
        unique.add(files[i]["hash"])

    log = "Deleted {0} duplicate files from {1} files.".format(count, total)
    return log


def main():
    """Main section"""
    print(remove_dup_files(arguments().parse_args()))


if __name__ == "__main__":
    main()
