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
__date__ = "13/07/2011"
__version__ = "0.3"

import os
import glob
import tarfile
import time
from get_size import get_size as _get_size
from get_size import best_unit_size as _best_unit_size
from logger import Logger as _logger
from notify import notify as _notify
from fabric.api import env, local

LOG = _logger()

#===============================================================================
# RSYNC HOSTS
#===============================================================================

# Your default host. No need any more if only wants a host.
env.host_string = "username@host"
env.remote = "/your/remote/path"
env.local = "/your/local/path"

# If wants to use various hosts, then define the previous variables like this, 
# one function per host. 
def _host_1():
    """Host variables for host_1."""
    global env
    env.host_string = "username@host_1"
    env.remote = "/your/remote/path/in/host_1"
    env.local = "/your/local/path/for/host_1"

def _host_2():
    """Host variables for host_2."""
    global env
    env.host_string = "username@host_2"
    env.remote = "/your/remote/path/in/host_2"
    env.local = "/your/local/path/for/host_2"

# ...
#
# def _host_n():
#     """Host variables for host_n."""
#     global env
#     env.host_string = "username@host_n"
#     env.remote = "/your/remote/path/in/host_n"
#     env.local = "/your/local/path/for/host_n"

#===============================================================================
# END RSYNC HOSTS
#===============================================================================

def _log_start():
    """Create the Start time info block for the log."""
    # Init the log for multiple hosts. Do not repeat the previous logs.
    if LOG.get():
        LOG.__init__()
    LOG.time("Start time")

def _log_end(task):
    """Create the End time info block and send & write the log."""
    _notify("Rsync", "Ended" , "ok")
    LOG.time("End time")
    LOG.free(os.linesep * 2)
    LOG.write(True)
    LOG.send("Fabric Rsync ({0})".format(task))

def _check_local():
    """Create local directory if no exists."""
    if not os.path.exists(env.local):
        os.mkdir(env.local)

def _rsync(source, target, delete):
    """Process the _rsync command."""
    _log_start()
    LOG.header("Fabric Rsync\nhttp://code.joedicastro.com/python-recipes",
               "Syncing {0} to {1}".format(source, target))
    _notify("Rsync", "Start syncing {0} to {1}".format(source, target), "info")
    out = local("rsync -pthrvz {2} {0}/ {1}".
                format(source, target, "--delete" if delete == "yes" else ""),
                capture=True)
    _notify("Rsync", "Finished synchronization", "ok")
    LOG.list("Rsync Output", out)
    if out.failed:
        LOG.list("Rsync Errors", out.stderr)

def _compress(path):
    """Compress a local directory into a gz file.

    Creates a file for each weekday, an removes the old files if exists"""
    os.chdir(os.path.join(path, os.pardir))
    dir2gz = os.path.basename(path)
    old_gzs = glob.glob('{0}*{1}.tar.gz'.format(dir2gz, time.strftime('%a')))
    gz_name = "{0}_{1}.tar.gz".format(dir2gz, time.strftime('%d%b%Y_%H:%M_%a'))
    gz_file = tarfile.open(gz_name, "w:gz")
    gz_file.add(path, arcname=dir2gz)
    gz_file.close()
    output = os.linesep.join(['Created file:', '', os.path.join(os.getcwd(),
                                                                gz_name)])
    for old_gz in old_gzs:
        os.remove(old_gz)
        output += os.linesep.join([os.linesep, 'Deleted old file:', '', old_gz])
    return output

def _archive():
    """Archive the local directory in a gz file for each weekday."""
    _notify('Rsync', 'Compressing folder...', 'info')
    LOG.list('Rotate compressed copies', _compress(env.local))
    _notify("Rsync", "Finished compression", "ok")

def _get_diskspace():
    """Get the disk space used by the local directory and archives."""
    gz_size = sum([_get_size(gz) for gz in glob.glob('{0}*.gz'.
                                                     format(env.local))])
    log_size = _get_size(LOG.filename) if os.path.exists(LOG.filename) else 0
    local_size = _get_size(env.local)
    size = _best_unit_size(local_size + gz_size + log_size)
    LOG.block('Disk space used', '{0:>76.2f} {1}'.format(size['s'], size['u']))

def up(server=None, dlt='yes'):
    """Sync from local to remote."""
    globals()["_" + server]() if server else None
    _rsync(env.local, ":".join([env.host_string, env.remote]), dlt)
    _log_end(server)

def down(server=None, dlt='yes', archive=False):
    """Sync from remote to local."""
    globals()["_" + server]() if server else None
    _check_local()
    _rsync(":".join([env.host_string, env.remote]), env.local, dlt)
    if not archive:
        _log_end(server)

def backup(server=None):
    """Sync from remote to local & archive the local directory."""
    down(server, archive=True)
    _archive()
    _get_diskspace()
    _log_end(server)

