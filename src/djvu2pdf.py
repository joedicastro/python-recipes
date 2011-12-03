#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    djvu2pdf.py: Converts a .djvu file into a .pdf file
"""

#==============================================================================
# This Script does exactly as the description above says.
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
__date__ = "03/12/2011"
__version__ = "0.3"

try:
    import sys
    import os
    from argparse import ArgumentParser
    from subprocess import Popen, PIPE
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def check_execs(*progs):
    """Check if the programs are installed, if not exit and report."""
    for prog in progs:
        try:
            Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
        except OSError:
            msg = 'The {0} program is necessary to run the script'.format(prog)
            sys.exit(msg)
    return


def arguments():
    """Defines the command line arguments for the script."""
    main_desc = """Converts a djvu file into a pdf file"""

    parser = ArgumentParser(description=main_desc)
    parser.add_argument("file", nargs="+", help="The djvu file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", dest="qlty", action="store_const", const="-d",
                        help="no compression. Best quality but big files.")
    group.add_argument("-z", dest="qlty", action="store_const", const="-z",
                        help="zip compression. More quality, more size.")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {0}".format(__version__),
                        help="show program's version number and exit")
    return parser


def process(command, fname):
    """Process the external commands and report the errors."""
    errors = Popen(command, stderr=PIPE).stderr.readlines()
    for line in errors:
        print("{0}: {1}".format(fname.upper(), line.rstrip(os.linesep)))


def main():
    """Main section."""
    args = arguments().parse_args()
    djvu_files = args.file

    for djvu in djvu_files:
        if not os.path.exists(djvu):
            print("ERROR: cannot open '{0}' (No such file)".format(djvu))
        else:
            djvu_filename = djvu.split(".djvu")[0]
            tiff = '{0}.tif'.format(djvu_filename)
            pdf = '{0}.pdf'.format(djvu_filename)
            process(['ddjvu', '-format=tiff', djvu, tiff], tiff)
            if os.path.exists(tiff):
                quality = args.qlty if args.qlty else "-j"
                process(['tiff2pdf', quality, '-o', pdf, tiff], pdf)
                os.remove(tiff)


if __name__ == "__main__":
    check_execs('ddjvu', 'tiff2pdf')
    main()
