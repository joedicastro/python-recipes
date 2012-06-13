#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
   dpkg_diff.py: Report changes in the packages installed on a debian based sys
"""

#==============================================================================
# This script is intended to run periodically through cron. This generates a
# list of packages installed on your system, and compares it with the one
# generated in the previous run. If there are differences, then generates a
# report that is saved to disk and sent by mail to the user who scheduled the
# cron job. It checks the Linux Debian packaging system, and therefore works on
# Debian and Debian based distros (Ubuntu, Mint, Mepis, ...)
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
__date__ = "06/05/2011"
__version__ = "0.1"

try:
    import sys
    import os
    import time
    import platform
    from re import findall, split
    from subprocess import Popen, PIPE
    from difflib import unified_diff
    from logger import Logger
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def pretty_diff(diff):
    """Better format for package lines in diff."""
    pkg = {}  # diff's packages lines

    # Get columns info for diff package lines
    for idx, line in enumerate(diff):
        if not findall("^-{3}|^\+{3}|^@{2}", line):
            # split the line in columns and remove the description column
            cols = split("\s{2,}", line, 3)[:3]
            # A nested dict, for each line index we have a dict that contains
            # the package line columns: 's' (status), 'n' (name) & 'v'
            # (version) and the width of the name column: w(width)
            pkg[idx] = {'s': cols[0], 'n': cols[1], 'v': cols[2],
                        'w': len(cols[1])}

    # maximum width in packages' name column for all lines
    mxw = max((pkg[index]['w'] for index in pkg))

    # Replace each package line for a prettier one (more legible)
    for i in range(len(diff)):
        if i in pkg:
            diff[i] = ("{0} {1} {2}".format(pkg[i]['s'], pkg[i]['n'] + " " *
                                            (mxw - pkg[i]['w']), pkg[i]['v']))
    return diff


def main(old=""):
    """Main section"""

    # The path to store the debian packages list file
    pkg_lst_file = "./package_list.txt"

    # Start logging
    log = Logger()
    url = "http://code.joedicastro.com/python-recipes"
    head = "Changes of packages installed on {0}".format(platform.node())
    log.header(url, head)
    log.time("Start time")

    # Read the old file and clean the list
    if os.path.exists(pkg_lst_file):
        old = open(pkg_lst_file, 'r').readlines()
        old_date = time.ctime(os.stat(pkg_lst_file).st_mtime)

    # Get the current list of debian packages installed on system
    current = Popen(["dpkg", "-l"], stdout=PIPE).stdout.readlines()

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
            log.list("Changes diff", pretty_diff(diff))
            log.time("End time")
            log.write(True)
            # Send mail to current system user. For other options, see logger
            # module info
            log.send("Debian packages changes")

if __name__ == "__main__":
    main()
