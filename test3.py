#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rusts.py Display information related to online players
and server version for the GamingOnLinux server.
Should be compatible with any source server/game"""

import valve.source.a2s
try:
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
except ImportError:
    print("Notify missing. Will print in terminal.")

def notification_send(summary, body):
    try:
        Notify.init("Rusts.py")
        notification = Notify.Notification.new(
            summary,
            body, # Optional
        )
        notification.show()
    except:
        print("{}: {}".format(summary, body))


if __name__ == "__main__":
    #player_list((SERVER, PORT))
    notification_send("Test", "Test!")
