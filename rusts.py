#!/usr/bin/env python2
import valve.source.a2s

SERVER="163.172.17.175"
PORT=30616

def playerList(server):
    server = valve.source.a2s.ServerQuerier(server)
    info = server.info()
    players = server.players()

    for p in players['players']:
        if p["name"]:
            print(p["name"]) + " (" + str(int((p["duration"]))) + "s)"

if __name__ == "__main__":
    playerList((unicode(SERVER, PORT)))
