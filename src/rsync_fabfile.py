#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
     A Fabric file for sync two directories (remote ⇄ local) with rsync.
"""

#===============================================================================
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
#===============================================================================

__author__ = "joe di castro <joe@joedicastro.com>"
__license__ = "GNU General Public License version 3"
__date__ = "06/07/2011"
__version__ = "0.1"


from logger import Logger as _logger
from notify import notify as _notify
from fabric.api import env, local

env.host_string = "username@host"
REMOTE_PATH = "/your/remote/path"
LOCAL_PATH = "/your/local/path"

def _rsync(source, target, delete):
    """Process the _rsync command."""
    log = _logger()
    log.header("Fabric Rsync\nhttp://code.joedicastro.com/python-recipes",
               "Syncing {0} to {1}".format(source, target))
    log.time("Start time")
    _notify("Rsync", "Start syncing {0} to {1}".format(source, target), "info")
    output = local("rsync -pthrvz {0}/ {1} {2}".
                   format(source, target, "--delete" if delete == "yes" else ""),
                   capture=True)
    _notify("Rsync", "Finished", "ok")
    log.list("Output", output)
    if output.failed:
        log.list("Error", output.stderr)
    log.time("End time")
    log.send("Fabric Rsync")

def up(dlt='yes'):
    """Sync from local to remote."""
    _rsync(LOCAL_PATH, ":".join([env.host_string, REMOTE_PATH]), dlt)

def down(dlt='yes'):
    """Sync from remote to local."""
    _rsync(":".join([env.host_string, REMOTE_PATH]), LOCAL_PATH, dlt)

