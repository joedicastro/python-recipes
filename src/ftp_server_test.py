#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    ftp_server_test.py: Create a ftp server for test purposes.
"""

#==============================================================================
# Create a ftp server for test purposes.
#
# Use Python FTP server library Project (pyftpdlib) by Giampaolo Rodola
# <g.rodola@gmail.com> at http://code.google.com/p/pyftpdlib/
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
    from pyftpdlib import ftpserver
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def ftp_server(ftp_dir, user, password):
    """Start a local ftp server."""
    authorizer = ftpserver.DummyAuthorizer()
    authorizer.add_user(user, password, ftp_dir, "elradfmw", "hi!", "bye")
    authorizer.add_anonymous(ftp_dir)
    handler = ftpserver.FTPHandler
    handler.authorizer = authorizer
    address = "127.0.0.1", 2121  # use 2121 to avoid security policies conflict
    ftpd = ftpserver.FTPServer(address, handler)
    ftpd.serve_forever()


def main():
    """Main section."""

    ftp_dir = "test"
    user = "user"
    password = "password"

    if not os.path.exists(ftp_dir):
        os.mkdir(ftp_dir)

    ftp_server(ftp_dir, user, password)

if __name__ == "__main__":
    main()
