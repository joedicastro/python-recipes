#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    ftp_upload.py: A method to upload a file to a FTP server.
"""

#==============================================================================
# A method to upload a file to a FTP server.
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
__date__ = "24/12/2010"
__version__ = "0.1"

try:
    import sys
    import os
    from ftplib import FTP

except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def upload_ftp(host, ftp_user, ftp_pass, ftp_dir, to_upload, port=21):
    """Upload by FTP a file to a host."""
    with open(to_upload, 'r') as file_2_upload:
        ftp = FTP()
        ftp.connect(host, port)
        ftp.login(ftp_user, ftp_pass)
        ftp.cwd(ftp_dir)
        ftp.storbinary('STOR {0}'.format(os.path.basename(to_upload)),
                       file_2_upload)
        ftp.quit()


def main():
    """Main section"""

    # To test this, first run ftp_server_test.py
    upload_ftp("localhost", "user", "password", "", __file__, port=2121)

if __name__ == "__main__":
    main()
