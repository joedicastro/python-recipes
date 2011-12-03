#!/usr/bin/env python
# -*- coding: <utf8> -*-

"""
    djvu2pdf.py:
"""

#===============================================================================
# This Script does...
#===============================================================================

#===============================================================================
#       Copyright 2009 joe di castro <joe@joedicastro.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#===============================================================================

__author__ = "joe di castro - joe@joedicastro.com"
__license__ = "GNU General Public License version 2"
__date__ = "16/06/2009"
__version__ = "0.1"

try: 
    import sys
    import os
    import optparse
    import re
    import subprocess

except ImportError:
    print ("""An error found importing one or more modules:
    \n{0}
    \nYou need to install this module\nQuitting...""").format(sys.exc_info()[1])
    sys.exit(-2)
    
def check_execs():
    """Check if the programs are installed """
    msg = 'The ddjvu and tiff2pdf programs are necessary to run this script.'
    try:
        pipe = subprocess.PIPE
        subprocess.Popen(['ddjvu', '--help'], stdout=pipe, stderr=pipe)
        subprocess.Popen(['tiff2pdf', '--help'], stdout=pipe, stderr=pipe)
    except OSError:
        sys.exit(msg)
    return


def options():
    """Defines the command line arguments and options for the script"""
    usage = """usage: %prog file.djvu"""
    desc = "Converts a djvu file into a pdf file"
    parser = optparse.OptionParser(usage=usage, version="%prog " + __version__,
                                   description=desc)
    return parser


def main():
    (opts, args) = options().parse_args()
    output = []
    if not args:
        sys.exit()
    else:
        djvu_file = args[0]
        filename = re.findall("(.+).djvu", djvu_file)[0]
    command_tif = ['ddjvu', '-format=tiff', '{0}.djvu'.format(filename),
                   '{0}.tif'.format(filename)]
    to_tiff = subprocess.Popen(command_tif, stdout=subprocess.PIPE)
    output.append(to_tiff.stdout.readlines())
    command_pdf = ['tiff2pdf', '-j', '-o', '{0}.pdf'.format(filename),
                    '{0}.tif'.format(filename)]
    to_pdf = subprocess.Popen(command_pdf, stdout=subprocess.PIPE)
    output.append(to_pdf.stdout.readlines())
    for line in output:
        if line:
            print line
    os.remove('{0}.tif'.format(filename))

if __name__ == "__main__":
    check_execs() # Check first if programs are installed
    main()
