#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    dir_size_monitor.py: Monitors changes in the size of dirs for a given path
"""

#===============================================================================
# This Script monitors the changes in disk size for the directories included in
# a given path. It reports what directories are new or deleted. Also reports the
# directories in which their size increases or decreases above threshold values.
# These threshold values refer to the amount in difference of size of the 
# directory or/and the percentage difference. These values can be overrided by 
# setting them to zero.
#
# The final report is sended via email to the local user. This script is 
# intended to run periodically (e.g. via cron) 
#===============================================================================

#===============================================================================
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
#===============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "16/05/2011"
__version__ = "0.1"

try:
    import sys
    import os
    import platform
    import pickle
    import logger
    from get_size import best_unit_size, get_size_fast
except ImportError:
    # Checks the installation of the necessary python modules 
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def list4log(dirs_size_dict, wpath, dirs):
    """Create a list of new or deleted directories for the log."""
    llst = []
    for ldir in sorted(dirs):
        dsz = best_unit_size(dirs_size_dict[ldir])
        llst.append(" {0:8.2f} {1}   ./{2}".
                    format(dsz['s'], dsz['u'], os.path.relpath(ldir, wpath)))
    return llst

def diff4log(before, current, wpath, dirs, threshold_pct=0, threshold_sz=0):
    """Create a list of the directories that had size changes for the log."""
    llst = []
    for ddir in sorted(dirs):
        pct = (((current[ddir] - float(before[ddir])) / before[ddir]) * 100.0)
        diff = current[ddir] - before[ddir]
        if pct >= threshold_pct and diff > threshold_sz:
            dsz = best_unit_size(diff)
            llst.append(" {0:8.2f} % {1:8.1f} {2}   ./{3}".
                        format(pct, dsz['s'], dsz['u'], os.path.relpath(ddir,
                                                                        wpath)))
    return llst


def main():
    """Main section"""
    # The path to monitor changes in directories dir_size
    mon_pth = "/your/path/to/monitor"

    # Ignore all directories that are below these percentage or absolute value 
    # of size difference. There are optional, set to zero to override them.
    thld_pct = 20      # In percentage of difference in size for a directory
    thld_sz = 10.486E6 # In bytes of absolute value of directory size difference

    # Prepare the log
    log = logger.Logger()
    url = "http://code.joedicastro.com/python-recipes"
    head = ("Changes in size of directories for {0} on {1}".
            format(mon_pth, platform.node()))
    log.header(url, head)
    log.time("START TIME")

    # Load the last dictionary of directories/sizes if exists
    try:
        with open('dir_sizes.pkl', 'rb') as input_file:
            bfr_dir = pickle.load(input_file)
    except (EOFError, IOError, pickle.PickleError):
        bfr_dir = {}

    # Get the current dictionary of directories/sizes
    crr_dir = {}
    for path, dirs, files in os.walk(mon_pth):
        for directory in dirs:
            dir_path = os.path.join(path, directory)
            dir_size = get_size_fast(dir_path)
            crr_dir[dir_path] = dir_size

    # First, Save the current dirs/sizes
    with open("dir_sizes.pkl", "wb") as output_file:
        pickle.dump(crr_dir, output_file)

    # Create the list depending the status of directories
    deleted = [d for d in bfr_dir if d not in crr_dir]
    added = [d for d in crr_dir if d not in bfr_dir]
    changed = [d for d in crr_dir if d in bfr_dir if crr_dir[d] != bfr_dir[d]]


    log.list("Deleted directories", list4log(bfr_dir, mon_pth, deleted))
    log.list("New directories", list4log(crr_dir, mon_pth, added))
    log.list("Changed directories", diff4log(bfr_dir, crr_dir, mon_pth, changed,
                                             thld_pct, thld_sz))

    # If thresholds are nonzero, then report the values 
    if thld_pct or thld_sz:
        tsz = best_unit_size(thld_sz)
        log.list("Threshold Values",
                 ["The directories whose size differences are less than any of "
                  "these values are ignored:", "",
                  "Percentage: {0:6} %".format(thld_pct),
                  "Size:       {0:6.2f} {1}".format(tsz['s'], tsz['u'])])

    # Show some statistics for the analyzed path
    mon_pth_sz = best_unit_size(get_size_fast(mon_pth))
    log.list("{0} Statistics".format(mon_pth),
             ["{0:8} directories".format(len(crr_dir)),
              "{0:8.2f} {1}".format(mon_pth_sz['s'], mon_pth_sz['u'])])
    log.time("END TIME")
    log.send("Changes in size of directories")

if __name__ == "__main__":
    main()
