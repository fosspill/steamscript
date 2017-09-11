#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rustsdb.py Store information related to
   online players for the GamingOnLinux server.
   Should be compatible with any source server/game"""

import valve.source.a2s
import psycopg2
import os
import datetime

SERVER = "163.172.17.175"
PORT = 30616

# assumes players table has been already created:
#   create table players (id serial, name varchar, login timestamp,
#                         logout timestamp, last_seen timestamp, duration int);
# expects DBNAME and DBUSER to be set on environment:
#   DBNAME=rust_gol DBUSER=user PYTHONPATH=~/git/python-valve/ python3 rusts.py dbstore
def store_to_db():
    """Store players info to a postgres database
       table columns: currenttime, name, duration"""

    try:
        players = valve.source.a2s.ServerQuerier((SERVER, PORT)).players()['players']

    except Exception as e:
        print("Can't connect to server")
        print(e)

    else:
        try:
            # potser check de duration al primer run, per veure si esta connectat des de l'ultim
            dbname = os.environ['DBNAME']
            dbuser = os.environ['DBUSER']
            players_loggedin = ()

            conn = psycopg2.connect("dbname="+dbname+" user="+dbuser)
            cur = conn.cursor()
            for player in players:
                cur.execute("SELECT id FROM players WHERE logout IS NULL AND name = %s", (player['name'],))
                record = cur.fetchone()
                if record is None:
                    login = datetime.datetime.now() - datetime.timedelta(seconds=player['duration'])
                    query = ("INSERT INTO players (name, login, last_seen, duration) VALUES (%s, %s, %s, %s) RETURNING id")
                    cur.execute(query, (player['name'], login, datetime.datetime.now(), player['duration']))
                    conn.commit()
                    players_loggedin += (cur.fetchone()[0],)
                else:
                    cur.execute("UPDATE players SET last_seen = now() WHERE id = %s", (record[0],))
                    conn.commit()
                    players_loggedin += (record[0],)

            if len(players_loggedin) > 0:
                cur.execute("UPDATE players SET logout = last_seen WHERE logout IS NULL AND id NOT IN %s", (players_loggedin,))
                conn.commit()
            else:
                cur.execute("UPDATE players SET logout = last_seen WHERE logout IS NULL")
                conn.commit()

        except psycopg2.OperationalError as e:
            print("Uh oh, can't connect. Invalid dbname, user or password?")
            print(e)

if __name__ == "__main__":
    store_to_db()
