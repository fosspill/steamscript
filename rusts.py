#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rusts.py Display information related to online players
and server version for the GamingOnLinux server.
Should be compatible with any source server/game"""

import valve.source.a2s
import time

SERVER = "89.34.99.19"
PORT = 28015


def player_list(server):
    """Retrieve player and limited server/game information and print the results

       Specifically, this retrieves information re: a Rust server.

       ----------------------------
       Rust - ServerName.com
       ----------------------------
       Rust Version 1234 (60ms)
       ----------------------------
       Player1:       2 hr 40 min
       Player2:	      2 hr 52 min
       Player3:	      1 hr 59 min
       Player4:	      2 hr 39 min
      ----------------------------
       4 players / 50 max
      ----------------------------"""

    try:
        server = valve.source.a2s.ServerQuerier(server)
        players = server.players()
        num_players, max_players, server_name, version = server.info()["player_count"], \
                                                         server.info()["max_players"], \
                                                         server.info()["server_name"], \
                                                         server.info()["version"]
        ping = round(server.ping())
    except Exception as e:
        print(e)
        return

    line_sep = "-" * 28

    print(line_sep)
    print(server_name)
    print(line_sep)
    print("Rust Version {} ({}ms)".format(version, ping))
    print(line_sep)
    if len(players["players"]) > 0:
        longestplayername = len(max(players["players"], key=lambda player: len(player["name"]))["name"])
        for player in sorted(players["players"], key=lambda player: player["name"]):
            player_name = player["name"]
            player_minutes = int(player["duration"]) / 60
            player_hours, player_minutes = divmod(player_minutes, 60)
            printstr = " " * (longestplayername-len(player_name)) + player_name + ":\t"+"%d hr %02d min" % (player_hours, player_minutes)
            print (printstr)
    else:
        print ("Nobody Rusting away here :(")

    print(line_sep)
    print("%d players / %d max" % (num_players, max_players))
    print(line_sep)


if __name__ == "__main__":
    player_list((SERVER, PORT))

