#!/usr/bin/env python2
# -*- coding: utf8 -*-

"""
    check_execs.py: Check if an executable program is present in the system.
"""

#==============================================================================
# Check if an executable program is present in the system. Useful for those
# scripts that requires external programs and don't have an install process.
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
__date__ = "02/01/2011"
__version__ = "0.1"

try:
    import sys
    import os
    import platform
    from re import findall
    from subprocess import Popen, PIPE
except ImportError:
    # Checks the installation of the necessary python modules
    print((os.linesep * 2).join(["An error found importing one module:",
          str(sys.exc_info()[1]), "You need to install it", "Stopping..."]))
    sys.exit(-2)


# Only for POSIX platforms (UNIX, Linux, Solaris, Mac OS X, ...)
def check_execs(*progs):
    """Check if the programs are installed, if not exit and report."""
    for prog in progs:
        try:
            Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
        except OSError:
            msg = 'The {0} program is necessary to run this.'.format(prog)
            sys.exit(msg)
    return


# Valid for *NIX systems and Windows systems
def check_execs_posix_win(progs):
    """Check if the program is installed.

    Returns one  dictionary with 1+n pair of key/values:

    A fixed key/value:

    "WinOS" -- (boolean) True it's a Windows OS, False it's a *nix OS

    for each program in progs a key/value like this:

    "program"  -- (str or boolean) The Windows executable path if founded else
                                   '' if it's Windows OS. If it's a *NIX OS
                                   True if founded else False

    """
    execs = {'WinOS': True if platform.system() == 'Windows' else False}
    # get all the drive unit letters if the OS is Windows
    windows_drives = findall(r'(\w:)\\',
                             Popen('fsutil fsinfo drives', stdout=PIPE).
                             communicate()[0]) if execs['WinOS'] else None

    progs = [progs] if isinstance(progs, str) else progs
    for prog in progs:
        if execs['WinOS']:
            # Set all commands to search the executable in all drives
            win_cmds = ['dir /B /S {0}\*{1}.exe'.format(letter, prog) for
                        letter in windows_drives]
            # Get the first location (usually C:) where the executable exists
            for cmd in win_cmds:
                execs[prog] = (Popen(cmd, stdout=PIPE, stderr=PIPE, shell=1).
                               communicate()[0].split(os.linesep)[0])
                if execs[prog]:
                    break
        else:
            try:
                Popen([prog, '--help'], stdout=PIPE, stderr=PIPE)
                execs[prog] = True
            except OSError:
                execs[prog] = False
    return execs


def main():
    """Main section"""

    if platform.system() != 'Windows':
        check_execs('python')

    programs = ['python', 'vim', 'iexplore']
    execs = check_execs_posix_win(programs)
    if execs['WinOS']:
        for prog in programs:
            print("Program: {0:12}Exe: {1}".format(prog, execs[prog]))
    else:
        for prog in programs:
            print("Program: {0:12}Found: {1}".format(prog, execs[prog]))


if __name__ == "__main__":
    main()
