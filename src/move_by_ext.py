#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    move_by_ext.py: Move (or copy/remove) files by extension.
"""

#==============================================================================
# This script find files by a given extension into a directory hierarchy and
# then move (or copy/remove) all of them to the given destination path.
#
# It pretends to be an alternative to these UNIX equivalent commands (but also
# works on windows and with various extensions at same time):
#
#   find ./SRC -type f -name *.EXT -exec mv {} ./DEST \;
#
#   find ./SRC -type f -name *.EXT -exec cp {} ./DEST \;
#
#   find ./SRC -type f -name *.EXT -exec rm -f {} \;
#
#==============================================================================

#==============================================================================
#    Copyright 2011 joe di castro <joe@joedicastro.com>
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
__date__ = "26/04/2011"
__version__ = "0.1"

try:
    import sys
    import os
    import shutil
    from argparse import ArgumentParser
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def arguments():
    """Defines the command line arguments for the script."""
    cur_dir = os.path.curdir
    main_desc = """Move (or copy/remove) all files selected by extension into a
    directory tree to a destination directory."""
    usage = "%(prog)s ext [-s SRC] [-d DST] [-c | -r] [--help]"

    parser = ArgumentParser(description=main_desc, usage=usage)
    parser.add_argument("ext", nargs='+', help="the extension(s) of the files "
                        "to process. To use more than one extension, separate "
                        "them with a space")
    parser.add_argument("-s", "--src", dest="src", default=cur_dir, help="the "
                        "source path. Current dir if none is provided")
    parser.add_argument("-d", "--dst", dest="dst", default=cur_dir, help="the "
                        "destination path. Current dir if none is provided")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--copy", dest="cp", action="store_true",
                       help="copy all the files with the given extension(s) "
                       "to the destination directory.")
    group.add_argument("-r", "--remove", dest="rm", action="store_true",
                       help="remove all the files with the given extension(s)."
                       " Use with caution! remove also in the subdirectories")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {0}".format(__version__),
                        help="show program's version number and exit")
    return parser


def find_and_process(args, count=0, log=""):
    """Find the files by file extension and process (move/copy/remove) them."""

    def process(the_path, the_file):
        """Process each file."""
        processed = 0
        src_file = os.path.join(the_path, the_file)
        dst_file = os.path.join(args.dst, the_file)
        if args.rm:
            os.remove(src_file)
            processed = 1
        else:
            if not os.path.exists(dst_file):  # not replace if already exists
                if args.cp:
                    shutil.copy2(src_file, dst_file)
                else:
                    shutil.move(src_file, dst_file)
                processed = 1
        return processed

    if not os.path.exists(args.dst):
        os.mkdir(args.dst)
    for path, directories, files in os.walk(args.src):
        for fil in files:
            # ignore files without extension, can have the same name as the ext
            file_ext = fil.split('.')[-1] if len(fil.split('.')) > 1 else None
            # ignore dots in given extensions
            extensions = [ext.replace('.', '') for ext in args.ext]
            if file_ext in extensions:
                count += process(path, fil)

    opt = int("{0}{1}".format(int(args.rm), int(args.cp)), 2)
    log = "Files {0}: {1}".format({0: "moved", 1: "copied", 2: "removed"}[opt],
                                  count)
    return log


def main():
    """Main section"""
    print(find_and_process(arguments().parse_args()))


if __name__ == "__main__":
    main()
