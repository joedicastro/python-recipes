#!/usr/bin/env pythonThis script is about ...
# -*- coding: utf8 -*-

"""
    template.py: This script is about ...
"""

#==============================================================================
# This Script does...
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
__date__ = "13/06/2012"
__version__ = "0.1"

try:
    import sys
    import os

except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def main():
    """Main section"""
    pass

if __name__ == "__main__":
    main()

###############################################################################
#                                  Changelog                                  #
###############################################################################
#
# 0.1:
#
# * First attempt
#
