#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
    notify.py: Send notification status messages through libnotify.
"""

#===============================================================================
# Send notification status messages through libnotify. 
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
__date__ = "21/12/2010"
__version__ = "0.1"

# Notify it's not essential and libnotify it's not always installed (in Ubuntu &
# Debian it's optional) but it's very useful to show popup messages
try:
    import pynotify
    import gtk
    NOT_NOTIFY = False
except ImportError:
    NOT_NOTIFY = True

def notify(title, msg, status):
    """Send notification status messages through libnotify.

    Parameters:

    (str) title -- The notification title
    (str) msg -- The message to display into notification
    (str) status -- Type of notification status (ok|info|error|warm|ask|sync)

    """
    if NOT_NOTIFY:
        return
    if not pynotify.is_initted():
        pynotify.init(title)
    note = pynotify.Notification(title, msg)
    helper = gtk.Button()
    icons = {'ok':gtk.STOCK_YES, 'info':gtk.STOCK_DIALOG_INFO,
             'error':gtk.STOCK_DIALOG_ERROR, 'warm':gtk.STOCK_DIALOG_WARNING,
             'ask':gtk.STOCK_DIALOG_QUESTION, 'sync':gtk.STOCK_JUMP_TO}
    icon = helper.render_icon(icons[status], gtk.ICON_SIZE_BUTTON)
    note.set_icon_from_pixbuf(icon)
    note.show()


def main():
    """Main section"""
    notify('TEST', 'This is an Ok Message', 'ok')
    notify('TEST', 'This is an Info Message', 'info')
    notify('TEST', 'This is an Error Message', 'error')
    notify('TEST', 'This is a Warm Message', 'warm')
    notify('TEST', 'This is an Ask Message', 'ask')
    notify('TEST', 'This is an Sync Message', 'sync')


if __name__ == "__main__":
    main()
