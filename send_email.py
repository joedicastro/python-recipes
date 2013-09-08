#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    send_email.py: Various ways to send a email.
"""

#==============================================================================
# This file provides various ways to send a email with python.
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
__date__ = "19/10/2011"
__version__ = "0.2"

try:
    import sys
    import os
    import socket
    import smtplib
    import getpass
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import COMMASPACE, formatdate
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


# The most simple way, in a Unix platform, sending email to user's local
# mailbox via the local smtp server. Useful for scripts.
def send_mail_local(subject, text):
    """Send a mail to the user's local mailbox."""
    # Set the local mail address for the script' user
    email = "@".join([getpass.getuser(), socket.gethostname()])
    msg = ("From: {0}\nTo: {0}\nSubject: {1}\n{2}".format(email, subject,
                                                          text))
    server = smtplib.SMTP("localhost")
    server.sendmail(email, email, msg)
    server.quit()
    return


# This covers 80% of situations, rarely need more. Use the most common e-mail
# fields.
def send_mail(subject, text, send_from="", dest_to=None, server="localhost",
              port=25, user="", passwd=""):
    """Send a email with a local or an external SMTP server.

    Arguments:
        (str) subject -- the mail's subject
        (str) text -- the message's text
        (str) send_from -- a sender's email address (default "")
        (list) dest_to -- a list of receivers' email addresses (default None)
        (str) server -- the smtp server (default "localhost")
        (int) port --  the smtp server port (default 25)
        (str) user -- the smtp server user (default "")
        (str) passwd --the smtp server password (default "")

    If "send_from" or "dest_to" are empty or None, then script user's mailbox
    is assumed instead. Useful for logging scripts

    """
    local_email = "@".join([getpass.getuser(), socket.gethostname()])
    send_from = send_from if send_from else local_email
    dest_to = dest_to if dest_to else [local_email]

    dest_to_addrs = COMMASPACE.join(dest_to)  # receivers mails
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = send_from
    message["To"] = dest_to_addrs
    message["Date"] = formatdate(localtime=True)
    message.preamble = "You'll not see this in a MIME-aware mail reader.\n"
    message.attach(MIMEText(text))

    # initialize the mail server
    smtp_server = smtplib.SMTP()
    # Connect to mail server
    try:
        smtp_server.connect(server, port)
    except socket.gaierror:
        print("mail error", "Wrong server, are you sure is correct?")
    except socket.error:
        print("mail error", "Server unavailable or connection refused")
    # Login in mail server
    if server != "localhost":
        try:
            smtp_server.login(user, passwd)
        except smtplib.SMTPAuthenticationError:
            print("mail error", "Authentication error")
        except smtplib.SMTPException:
            print("mail error", "No suitable authentication method")
    # Send mail
    try:
        smtp_server.sendmail(send_from, dest_to_addrs, message.as_string())
    except smtplib.SMTPRecipientsRefused:
        print("mail error", "All recipients were refused."
              "Nobody got the mail.")
    except smtplib.SMTPSenderRefused:
        print("mail error", "The server didn’t accept the from_addr")
    except smtplib.SMTPDataError:
        print("mail error", "An unexpected error code, Data refused")
    # Disconnect from server
    smtp_server.quit()


# The more complete solution. This adds the Cc: (Carbon Copy) and Bcc: (Blind
# Carbon Copy) fields and the ability to add attachments.
def send_email(subject, text, send_from="", dest_to=None, attachments=None,
               send_cc=None, send_bcc=None, server="localhost", port=25,
               user="", passwd=""):
    """Send a email with(out) attachment(s) enabling CC and BCC fields.

    Arguments:
        (str) subject -- the mail's subject
        (str) text -- the message's text
        (str) send_from -- a sender's email address (default "")
        (list) dest_to -- a list of receivers' email addresses ("")
        (list) attachments -- a list of attachments files (default None)
        (list) send_cc -- a list of carbon copy's email addresses (def. None)
        (list) send_bcc -- a list of blind carbon copy's email addresses (None)
        (str) server -- the smtp server (default "localhost")
        (int) port -- the smtp server port (default 25)
        (str) user -- the smtp server user (default "")
        (str) passwd --the smtp server password (default "")

    If "send_from" or "dest_to" are empty or None, then script user's mailbox
    is assumed instead. Useful for logging scripts

    """
    local_email = "@".join([getpass.getuser(), socket.gethostname()])
    send_from = send_from if send_from else local_email
    dest_to = dest_to if dest_to else [local_email]

    dest_to_addrs = dest_to  # receivers mails including to, cc and bcc fields
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = send_from
    message["To"] = COMMASPACE.join(dest_to)
    if send_cc:
        message["Cc"] = COMMASPACE.join(send_cc)
        dest_to_addrs += send_cc
    if send_bcc:
        dest_to_addrs += send_bcc
    message["Date"] = formatdate(localtime=True)
    message.preamble = "You'll not see this in a MIME-aware mail reader.\n"
    message.attach(MIMEText(text))

    # For all type of attachments
    if attachments:
        for att_file in attachments:
            with open(att_file, "rb") as attmnt:
                att = MIMEBase("application", "octet-stream")
                att.set_payload(attmnt.read())
            encoders.encode_base64(att)
            att.add_header("content-disposition", "attachment",
                           filename=os.path.basename(att_file))
            message.attach(att)

    # initialize the mail server
    smtp_server = smtplib.SMTP()
    # Connect to mail server
    try:
        smtp_server.connect(server, port)
    except socket.gaierror:
        print("mail error", "Wrong server, are you sure is correct?")
    except socket.error:
        print("mail error", "Server unavailable or connection refused")
    # Login in mail server
    if server != "localhost":
        try:
            smtp_server.login(user, passwd)
        except smtplib.SMTPAuthenticationError:
            print("mail error", "Authentication error")
        except smtplib.SMTPException:
            print("mail error", "No suitable authentication method")
    # Send mail
    try:
        smtp_server.sendmail(send_from, dest_to_addrs, message.as_string())
    except smtplib.SMTPRecipientsRefused:
        print("mail error", "All recipients were refused."
              "Nobody got the mail.")
    except smtplib.SMTPSenderRefused:
        print("mail error", "The server didn’t accept the from_addr")
    except smtplib.SMTPDataError:
        print("mail error", "An unexpected error code, Data refused")
    # Disconnect from server
    smtp_server.quit()


def main():
    """Main section"""

    send_mail_local("Testing sending an email locally",
                    "If you can read this, your local smtp server is OK")
    send_mail("Testing sending an email locally changing the from address",
              "If you can read this, believe me, the King is dead. Sorry",
              send_from="elvis@heave.nz")
    send_email("Testing sending a email with an attachment",
               "If you can read this and the attachment, all is fine.",
               attachments=[__file__])

    print("Check the mail in your mailbox {0}".
          format("@".join([getpass.getuser(), socket.gethostname()])))

if __name__ == "__main__":
    main()
