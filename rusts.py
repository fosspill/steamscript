#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rusts.py Display information related to online players
and server version for the GamingOnLinux server.
Should be compatible with any source server/game"""

SERVER = "163.172.17.175"
PORT = 30616
SLEEP = 60 # seconds between server queries

import time
import os
import valve.source.a2s
from datetime import datetime
try:
    import gi
    gi.require_version('Notify', '0.7')
    from gi.repository import Notify
except ImportError:
    print("Notify missing. Will print in terminal.")

def notification_send(summary, body=''):
    try:
        Notify.init("Rusts.py")
        notification = Notify.Notification.new(
            summary,
            body, # Optional
        )
        notification.show()
    except:
        print("{}: {}".format(summary, body))

def player_list(last_players):
    """Retrieve player and limited server/game information and print the results

       Specifically, this retrieves information re: a Rust server.

       ----------------------------
       Rust - ServerName.com
       ----------------------------
       Rust Version 1234 (60ms)
       ----------------------------
       Player1:       2 hr 40 min
       Player2:       2 hr 52 min
       Player3:       1 hr 59 min
       Player4:       2 hr 39 min
      ----------------------------
       4 players / 50 max
      ----------------------------"""

    current_players = {}
    server = valve.source.a2s.ServerQuerier((SERVER, PORT))
    players = sorted(server.players()['players'], key=lambda player: player["name"])
    num_players, max_players, server_name, version = server.info()["player_count"], \
                                                     server.info()["max_players"], \
                                                     server.info()["server_name"], \
                                                     server.info()["version"]
    ping = round(server.ping())

    line_sep = "-" * 28

    print(line_sep)
    print(server_name)
    print(line_sep)
    print("Rust Version {} ({}ms)".format(version, ping))
    print(line_sep)

    for player in players:
        player_name = player["name"]
        player_minutes = int(player["duration"]) / 60
        player_hours, player_minutes = divmod(player_minutes, 60)
        print("%12s:\t %d hr %02d min" % (player_name[:12], player_hours, player_minutes))
        if last_players is not None:
            if player_name not in last_players:
                notification_send(player_name + " has logged in")
        current_players[player_name] = player

    if last_players is not None:
        for player in last_players.values():
            if player['name'] not in current_players:
                notification_send(player['name'] + ' has logged off')

    print(line_sep)
    print("%d players / %d max" % (num_players, max_players))
    print(line_sep)
    print("Last updated at %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return current_players


if __name__ == "__main__":
    try:
        last_players = None
        while True:
            os.system('clear')
            last_players = player_list(last_players)
            time.sleep(SLEEP)
    except KeyboardInterrupt:
        print('Bye!')
