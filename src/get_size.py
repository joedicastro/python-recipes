#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    get_dir_size.py: Various ways to calculate the size of a directory tree.
"""

#==============================================================================
# Various ways to calculate the size of a directory tree or a single file.
# Include methods to convert a size in bytes to the best standard IEC binary
# prefix to improve readability.
#
# The IEC (International Electrotechnical Commission) binary prefixes for
# quantities of digital information are these:
#
#    IEC binary prefixes      SI decimal prefixes          Equivalences
#  =======================  =======================  ========================
#   Prefix   Symbol bytes    Prefix   Symbol bytes    IEC prefix   SI prefix
#  ========  ====== =====   ========= ====== =====   ============ ===========
#
#  kibibyte   KiB    2¹⁰    kilobyte    kB    10³       1 KiB      1.024 kB
#  mebibyte   MiB    2²⁰    megabyte    MB    10⁶       1 MiB      1.049 MB
#  gibibyte   GiB    2³⁰    gigabyte    GB    10⁹       1 GiB      1.074 GB
#  tebibyte   TiB    2⁴⁰    terabyte    TB    10¹²      1 TiB      1.100 TB
#  pebibyte   PiB    2⁵⁰    petabyte    PB    10¹⁵      1 PiB      1.126 EB
#  exbibyte   EiB    2⁶⁰    exabyte     EB    10¹⁸      1 EiB      1.153 EB
#  zebibyte   ZiB    2⁷⁰    zettabyte   ZB    10²¹      1 ZiB      1.181 EB
#  yobibyte   YiB    2⁸⁰    yottabyte   YB    10²⁴      1 YiB      1.209 ZB
#
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
__date__ = "30/12/2010"
__version__ = "0.1"

try:
    import sys
    import os
    import time
    from subprocess import Popen, PIPE
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


# Not Mine, Seen out there. Approximate size, non accurate. Don't go in hidden
# files and dirs, and don't take into account the ".." especial files and
# symbolic links. No works with a single file
def get_dir_size(the_path):
    """Get size of a directory tree in bytes."""
    path_size = 0
    for path, dirs, files in os.walk(the_path):
        for fil in files:
            filename = os.path.join(path, fil)
            path_size += os.path.getsize(filename)
    return path_size


# My Version, accurate. Same results as *NIX command "du -bs". Take in
# consideration symbolic links and don't follow them. Works with single files
def get_size(the_path):
    """Get size of a directory tree or a file in bytes."""
    path_size = 0
    for path, directories, files in os.walk(the_path):
        for filename in files:
            path_size += os.lstat(os.path.join(path, filename)).st_size
        for directory in directories:
            path_size += os.lstat(os.path.join(path, directory)).st_size
    path_size += os.path.getsize(the_path)
    return path_size


# less pythonic, but faster and still accurate. Take in consideration the
# symbolic links and don't follow them
def get_size_fast(the_path):
    """Get size of a directory tree or a file in bytes."""

    def get_sizes(the_path):
        """Make a generator of individual file & directory sizes."""
        if not os.path.islink(the_path):
            if os.path.isdir(the_path):
                for file_or_dir in os.listdir(the_path):
                    path = os.path.join(the_path, file_or_dir)
                    if os.path.isfile(path):
                        yield os.lstat(path).st_size
                    else:
                        for size in get_sizes(path):
                            yield size
            yield os.lstat(the_path).st_size
        else:
            yield os.lstat(the_path).st_size

    return sum(get_sizes(the_path))


# This converts a size in bytes to the best unit, using IEC binary prefixes.
def best_unit_size(bytes_size):
    """Get a size in bytes & convert it to the best IEC prefix for readability.

    Return a dictionary with three pair of keys/values:

    "s" -- (float) Size of path converted to the best unit for easy read
    "u" -- (str) The prefix (IEC) for s (from bytes(2^0) to YiB(2^80))
    "b" -- (int / long) The original size in bytes

    """
    for exp in range(0, 90, 10):
        bu_size = abs(bytes_size) / pow(2.0, exp)
        if int(bu_size) < 2 ** 10:
            unit = {0: "bytes", 10: "KiB", 20: "MiB", 30: "GiB", 40: "TiB",
                    50: "PiB", 60: "EiB", 70: "ZiB", 80: "YiB"}[exp]
            break
    return {"s": bu_size, "u": unit, "b": bytes_size}


# Combination of calculating the size in bytes and conversion to best IEC
# prefix in one function.
def get_unit_size(the_path):
    """Calculate size of a directory/file & convert it for the best IEC prefix.

    Return a dictionary with three pair of keys/values:

    "s" -- (float) Size of path converted to the best unit for easy read
    "u" -- (str) The prefix (IEC) for s (from bytes(2^0) to YiB(2^80))
    "b" -- (int / long) The original size in bytes

    """

    bytes_size = 0
    for path, directories, files in os.walk(the_path):
        for filename in files:
            bytes_size += os.lstat(os.path.join(path, filename)).st_size
        for directory in directories:
            bytes_size += os.lstat(os.path.join(path, directory)).st_size
    bytes_size += os.path.getsize(the_path)

    for exp in range(0, 90, 10):
        bu_size = abs(bytes_size) / pow(2.0, exp)
        if int(bu_size) < 2 ** 10:
            unit = {0: "bytes", 10: "KiB", 20: "MiB", 30: "GiB", 40: "TiB",
                    50: "PiB", 60: "EiB", 70: "ZiB", 80: "YiB"}[exp]
            break
    return {"s": bu_size, "u": unit, "b": bytes_size}


class GetSize:
    """Create a GetSize object that converts size(bytes) to the best IEC prefix.

    The size of this object can be obtained from a path (directory or file) or
    from a size in bytes.

    """

    def __init__(self):
        """Create the object GetSize itself and set various attributes.

        These attributes are about the size of a file or directory tree:

        bytes = The size in bytes
        size = The size in the best IEC unit prefix for readability
        unit = The IEC prefix of size

        """
        self.bytes = 0
        self.size = 0
        self.unit = "bytes"

    def from_bytes(self, sz_bytes):
        """Get size & IEC prefix from size in bytes."""
        self.bytes = sz_bytes
        for exp in range(0, 90, 10):
            self.size = abs(self.bytes) / pow(2.0, exp)
            if int(self.size) < 2 ** 10:
                self.unit = {0: "bytes", 10: "KiB", 20: "MiB", 30: "GiB",
                             40: "TiB", 50: "PiB", 60: "EiB", 70: "ZiB",
                             80: "YiB"}[exp]
                break

    def from_path(self, a_path):
        """Get size & IEC prefix from a directory or file."""
        for path, directories, files in os.walk(a_path):
            for filename in files:
                self.bytes += os.lstat(os.path.join(path, filename)).st_size
            for directory in directories:
                self.bytes += os.lstat(os.path.join(path, directory)).st_size
        self.bytes += os.path.getsize(a_path)
        self.from_bytes(self.bytes)


def main():
    """Main section"""

    my_path = ".."

    functions = [get_dir_size, get_size, get_size_fast]

    def timeit(ftn, *args):
        """Get time consumed by a function."""
        time_start = time.time()
        sz_du = ftn(args[0])
        time_end = time.time()
        return sz_du, time_end - time_start

    # Show results from standard *NIX command 'du'
    print("  Space     in bytes       'du' Diff      Time")
    print("  =====     ========       =========      ====")
    print("$ du -bs".center(50) + os.linesep + ("-" * 8).center(50))
    tm_du_start = time.time()
    bytes_du = int(Popen(["du", "-bs", my_path], stdout=PIPE).stdout.
                   readlines()[0].split()[0])
    tm_du = time.time() - tm_du_start
    sz_du = best_unit_size(bytes_du)
    print("{0:.1f} {1} {2:12}         n/a {3:12.4f}s".
          format(sz_du["s"], sz_du["u"], sz_du["b"], tm_du) + os.linesep)

    # Show results of the distinct Python methods to compare speed & precision
    for fnct in functions:
        fname = fnct.__name__
        print(fname.center(50) + os.linesep + ("-" * len(fname)).center(50))
        bytes_fn, time_fn = timeit(fnct, my_path)
        sz_fn = best_unit_size(bytes_fn)
        diff_fn = best_unit_size(bytes_du - sz_fn["b"])
        print("{0:.1f} {1} {2:12} {3:10.2f} {4:5}{5:8.4f}s".
              format(sz_fn["s"], sz_fn["u"], sz_fn["b"], diff_fn["s"],
                     diff_fn["u"], time_fn) + os.linesep)

    # get_unit_size as a combination of two functions requires separate code
    print("get_unit_size".center(50) + os.linesep + ("-" * 13).center(50))
    sz_gus, tm_gus = timeit(get_unit_size, my_path)
    diff_gus = best_unit_size(bytes_du - sz_gus["b"])
    print("{0:.1f} {1} {2:12} {3:10.2f} {4:5}{5:8.4f}s".
          format(sz_gus["s"], sz_gus["u"], sz_gus["b"], diff_gus["s"],
                 diff_gus["u"], tm_gus) + os.linesep)

    # shows results from GetSize class
    print("GetSize Class".center(50) + os.linesep + ("-" * 13).center(50))
    time_class_start = time.time()
    sz_class = GetSize()
    sz_class.from_path(my_path)
    tm_class = time.time() - time_class_start
    diff_class = GetSize()
    diff_class.from_bytes(bytes_du - sz_class.bytes)
    print("{0:.1f} {1} {2:12} {3:10.2f} {4:5}{5:8.4f}s".
          format(sz_class.size, sz_class.unit, sz_class.bytes, diff_class.size,
                 diff_class.unit, tm_class) + os.linesep)


if __name__ == "__main__":
    main()
