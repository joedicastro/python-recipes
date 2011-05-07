#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    logger.py: Create a log object to log script messages in a elegant way
"""

#===============================================================================
# This module create a log object to log script messages in a elegant way
#===============================================================================

#===============================================================================
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
#===============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "10/09/2010"
__version__ = "0.3"

try:
    import sys
    import os
    import time
    import smtplib
    import socket
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import COMMASPACE, formatdate
except ImportError:
    # Checks the installation of the necessary python modules 
    print((os.linesep * 2).join(["An error found importing one module:",
    str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


class Logger():
    """

    Create a log object to log script messages.

    These messages can be sended via email or writed in a log file

    """

    def __init__(self):
        """Create the object Logger itself and set various attributes.

        These attributes are about the python file wich invokes this module:

        __script_vers = The version of python file which invokes this module
        __script_name = The name of the python file which invokes this module
        filename = the log file's name

        """
        from __main__ import __dict__ as __dict
        self.__log = ''
        if '__version__' in __dict.keys():
            self.__script_vers = __dict['__version__']
        else:
            self.__script_vers = 'Unknown'
        self.__script_name = os.path.basename(__dict['__file__']).split('.')[0]
        self.filename = '{0}.log'.format(self.__script_name)

    def __len__(self):
        return len(self.__log)

    def __format__(self, tit, cont, decor):
        """Format a block or a list of lines to enhance comprehension.

        (str) tit -- title for the block or list
        (str or iterable) cont -- line/s for the list/block content
        ('=' or '_') decor - define if it's list or block and decorate it

        make the looks of self.block() and self.list()

        """
        ending = {'=':'', '_':os.linesep}[decor]
        end = {'=': '=' * 80, '_':''}[decor]
        begin = ' '.join([tit.upper(), (80 - (len(tit) + 1)) * decor]) + ending
        cont = [cont] if isinstance(cont, str) else cont
        sep = os.linesep
        self.__log += sep.join([begin, sep.join(cont), end, sep])

    def block(self, title, content):
        """A block of text lines headed and followed by a line full of '='.

        (str) title -- The title that start the first line of '='
        (str or iterable) content -- The line/s between the '=' lines

        There's not any empty line between the '=' lines and content, e.g.:

        TITLE ==================================================
        content
        ========================================================

        """
        if content:
            self.__format__(title, content, '=')

    def list(self, title, content):
        """A list of text lines headed by a line full of '_'.

        (str) title -- The title that start the line of '_'
        (str or iterable) content -- The line/s after the '_' line

        After the '_' line is a empty line between it and the content, e.g.:

        TITLE __________________________________________________

        content

        """
        if content:
            self.__format__(title, content, '_')

    def free(self, content):
        """Free text unformatted.

        (str) content -- Text free formated

        """
        if isinstance(content, str):
            self.__log += content + os.linesep * 2

    def time(self, title):
        """A self.block() formated line with current time and date.

        (str) title -- Title for self.block()

        Looks like this, the data and time are right-justified:

        TITLE ==================================================
                                       Friday 09/10/10, 20:01:39
        ========================================================

        """
        self.block(title, '{0:>80}'.format(time.strftime('%A %x, %X')))

    def header(self, url, msg):
        """A self.block() formated header for the log info.

        (str) url -- The url of the script
        (str) msg -- Message to show into the header. To Provide any useful info

        It looks like this:

        SCRIPT =================================================
        script name and version
        url

        msg
        ========================================================

        """
        script = '{0} (ver. {1})'.format(self.__script_name, self.__script_vers)
        self.block('Script', [script, url, '', msg])

    def get(self):
        """Get the log content."""
        return self.__log

    def send(self, subject, send_from='', dest_to='', mail_server='localhost',
             server_user='', server_pass=''):
        """Send a email with the log.

        Arguments:
            (str) send_from -- a sender's email address (default '')
            (str or list) dest_to -- a list of receivers' email addresses ('')
            (str) subject -- the mail's subject
            (str) mail_server -- the smtp server (default 'localhost')
            (str) server_user -- the smtp server user (default '')
            (str) server_pass --the smtp server password (default '')

        If 'send_from' or 'dest_to' are empty or None, then script user's
        mailbox is assumed instead. Useful for loggin scripts

        """
        local_email = '@'.join([os.getenv('LOGNAME'), socket.gethostname()])
        if not send_from:
            send_from = local_email
        if not dest_to:
            dest_to = [local_email]

        dest_to_addrs = COMMASPACE.join(dest_to) # receivers mails
        message = MIMEMultipart()
        message['Subject'] = '{0} - {1}'.format(subject,
                                                time.strftime('%A %x, %X'))
        message['From'] = send_from
        message['To'] = dest_to_addrs
        message['Date'] = formatdate(localtime=True)
        message.preamble = "You'll not see this in a MIME-aware mail reader.\n"
        message.attach(MIMEText(self.__log))

        # initialize the mail server
        server = smtplib.SMTP()
        # Connect to mail server
        try:
            server.connect(mail_server)
        except socket.gaierror:
            self.list('mail error', 'Wrong server, are you sure is correct?')
        except socket.error:
            self.list('mail error', 'Server unavailable or connection refused')
        # Login in mail server
        if mail_server != 'localhost':
            try:
                server.login(server_user, server_pass)
            except smtplib.SMTPAuthenticationError:
                self.list('mail error', 'Authentication error')
            except smtplib.SMTPException:
                self.list('mail error', 'No suitable authentication method')
        # Send mail
        try:
            server.sendmail(send_from, dest_to_addrs, message.as_string())
        except smtplib.SMTPRecipientsRefused:
            self.list('mail error', 'All recipients were refused.'
                      'Nobody got the mail.')
        except smtplib.SMTPSenderRefused:
            self.list('mail error', 'The server didn’t accept the from_addr')
        except smtplib.SMTPDataError:
            self.list('mail error', 'An unexpected error code, Data refused')
        # Disconnect from server
        server.quit()

    def write(self, append=False):
        """Write the log to a file.

        The name of the file will be like this:

        script.log

        where 'script' is the name of the script file without extension (.py)

        (boolean) append -- If true appends log to file, else writes a new one

        """
        mode = 'ab' if append else 'wb'
        with open(self.filename, mode) as log_file:
            log_file.write(self.__log)


def main():
    """Main section"""
    url = 'http://code.joedicastro.com/python-recipes'
    head = 'This is a test of class Logger'

    log = Logger()
    log.header(url, head)
    log.time('Start time')
    log.block('Block', 'This is a sample of Logger.block()'.split())
    log.list('List', 'This is a sample of Logger.list()'.split())
    log.free('''This a sample of logger.free() text.
    
"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque sed
tortor eget justo vehicula consequat vel eu quam. Suspendisse non lectus eget
orci varius adipiscing."''')
    log.time('End time')
    log.send('This is mail test')
    log.write(True)
    log.free('All of this had been recorded in {0}'.format(log.filename))
    print(log.get())


if __name__ == "__main__":
    main()
