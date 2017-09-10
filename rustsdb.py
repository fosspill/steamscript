#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rustsdb.py Store information related to
   online players for the GamingOnLinux server.
   Should be compatible with any source server/game"""

import valve.source.a2s
import psycopg2
import psycopg2.extras
import os

SERVER = "163.172.17.175"
PORT = 30616

# assumes players table has been already created:
#   create table players (currenttime timestamp, name varchar, duration int);
# expects DBNAME and DBUSER to be set on environment:
#   DBNAME=rust_gol DBUSER=user PYTHONPATH=~/git/python-valve/ python3 rusts.py dbstore
def store_to_db():
    """Store players info to a postgres database
       table columns: currenttime, name, duration"""

    try:
        players = valve.source.a2s.ServerQuerier((SERVER, PORT)).players()

        players_data = list(map(lambda player: (
            'now()', player["name"], int(player["duration"])
            ), players["players"]))

    except Exception as e:
        print("Can't connect to server")
        print(e)

    else:
        try:
            dbname = os.environ['DBNAME']
            dbuser = os.environ['DBUSER']
            insert_query = 'INSERT INTO players (currenttime, name, duration) VALUES %s'
            conn = psycopg2.connect("dbname="+dbname+" user="+dbuser)
            cur = conn.cursor()
            psycopg2.extras.execute_values (cur, insert_query, players_data)
            conn.commit()

        except Exception as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)

if __name__ == "__main__":
    store_to_db()

