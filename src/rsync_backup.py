#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    rsync_backup.py: Make a backup via Rsync. Intended to be used periodically
    in a cron job to maintain a local backup of a path in an another
    localization (e.g. another drive) and to take advantage of the rsync's
    speed and minimal footprint. It's ideal for those cases in which a RAID 1,
    a regular backup app or a DCVS may not be the best option to maintain a
    mirrored copy.
"""

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "07/02/2013"
__version__ = "0.1"


try:
    import sys
    import os
    from argparse import ArgumentParser
    from subprocess import Popen, PIPE
    from logger import Logger
    from notify import notify
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


def arguments():
    """Defines the command line arguments for the script."""
    main_desc = """Make a backup via rsync"""

    parser = ArgumentParser(description=main_desc)
    parser.add_argument("source", help="the source path")
    parser.add_argument("backup", help="the backup path")
    parser.add_argument("-n", dest="notify", action="store_true",
                        help="show popup notifications")
    parser.add_argument("-s", dest="send", action="store_true",
                        help="send a log via mail to the current local user")
    parser.add_argument("-v", "--version", action="version",
                        version="%(prog)s {0}".format(__version__),
                        help="show program's version number and exit")
    return parser


def main():
    """Main section"""
    args = arguments().parse_args()
    options = "-azxhvP --delete --ignore-errors --stats"
    command = "rsync {2} {0} {1}/".format(args.source, args.backup, options)

    log = Logger()
    url = "http://joedicastro.com"
    head = "Backup of {0} into {1}".format(args.source, args.backup)
    log.header(url, head)

    log.time('Start Backup')
    if args.notify:
        notify('Rsync Backup', 'Starting backup of {0} into {1}'.
                               format(args.source, args.backup), 'info')

    rsync = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    out, errors = rsync.stdout.read(), rsync.stderr.read()
    log.list('Rsync output', out)
    if errors:
        log.list('Errors', errors)

    log.time('End Backup')
    if args.notify:
        notify('Rsync Backup', 'Backup ended', 'ok')

    if args.send:
        log.send('Rsync backup')
    log.write(True)


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
