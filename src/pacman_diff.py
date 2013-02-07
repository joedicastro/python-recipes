#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
   pacman_diff.py: Report changes in the packages installed on a Arch based sys
"""

#==============================================================================
# This script is intended to run periodically through cron. This generates a
# list of packages installed on your system, and compares it with the one
# generated in the previous run. If there are differences, then generates a
# report that is saved to disk and sent by mail to the user who scheduled the
# cron job. It checks the Linux Arch packaging system, and therefore works on
# Arch and Arch based distros (Chakra, ArchBang, Parabola, ...)
#==============================================================================

#==============================================================================
#    Copyright 2012 joe di castro <joe@joedicastro.com>
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
__date__ = "21/11/2012"
__version__ = "0.2"

try:
    import os
    import platform
    import sys
    import time
    from argparse import ArgumentParser
    from difflib import unified_diff
    from logger import Logger
    from subprocess import Popen, PIPE
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def arguments():
    """Defines the command line arguments for the script."""
    desc = """Report changes in the packages installed on a Arch based sys"""

    parser = ArgumentParser(description=desc)
    parser.add_argument("path", default='./package_list.txt', nargs='?',
                        help="The path to store the arch packages list file")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {0}".format(__version__),
                        help="show program's version number and exit")
    return parser


def main(old=""):
    """Main section"""

    # The path to store the arch packages list file
    args = arguments().parse_args()
    pkg_lst_file = args.path

    # Start logging
    log = Logger()
    url = "http://joedicastro.com"
    head = "Changes of packages installed on {0}".format(platform.node())
    log.header(url, head)
    log.time("Start time")

    # Read the old file and clean the list
    if os.path.exists(pkg_lst_file):
        old = open(pkg_lst_file, 'r').readlines()
        old_date = time.ctime(os.stat(pkg_lst_file).st_mtime)

    # Get the current list of arch packages installed on system
    current = Popen(["pacman", "-Q"], stdout=PIPE).stdout.readlines()

    # First, save the list file
    with open(pkg_lst_file, 'w') as out:
        out.writelines(current)
        curr_date = time.ctime(os.stat(pkg_lst_file).st_mtime)

    # Compare both lists
    if old:
        file_path = os.path.realpath(pkg_lst_file)
        diff = [ln for ln in unified_diff(old, current, fromfile="previous",
                                          tofile="current ",
                                          fromfiledate=old_date,
                                          tofiledate=curr_date, n=0,
                                          lineterm="")]

        # If there are differences write the log to disk and send mail
        if diff:
            log.list("Installed packages list file", file_path)
            log.list("Changes diff", diff)
            log.time("End time")
            log.write(True)
            # Send mail to current system user. For other options, see logger
            # module info
            log.send("Arch packages changes")

if __name__ == "__main__":
    main()
