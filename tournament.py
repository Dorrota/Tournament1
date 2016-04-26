#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


# Database connection
def connect():
    return psycopg2.connect("dbname=tournament")


# Remove all the match records from the database
def deleteMatches():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from matches")
    DB.commit()
    DB.close()


# Remove all the player records from the database
def deletePlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE from players")
    DB.commit()
    DB.close()


# Returns the number of registered players
def countPlayers():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT count(*) from players")
    pl_count = c.fetchone()[0]
    print pl_count
    DB.close()
    return pl_count


# Adds a player to the tournament database
def registerPlayer(name):
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO players (pl_name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()


# Returns a list of the players and their win records, sorted by wins
def playerStandings():
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT pl_wins.pl_id, pl_wins.pl_name, pl_wins.wins, wins+loose as nr_matches from pl_wins order by wins desc")
    standing = c.fetchall()
    DB.close()
    return standing


# Records the outcome of a single match between two players
def reportMatch(winner, loser):
    DB = connect()
    c = DB.cursor()
    next_match = ("INSERT INTO matches (win_pl_id, loose_pl_id) VALUES (%s, %s) ")
    c.execute(next_match, (winner, loser))
    DB.commit()
    DB.close()


# Returns a list of pairs of players for the next round of a match
def swissPairings():
    standing = playerStandings()
    i = 0
    pairing = []
    tupla = ()
    while i < len(standing):
        tupla = (standing[i][0], standing[i][1],
                 standing[i+1][0], standing[i+1][1])
        pairing.append(tupla)
        i = i + 2
    return pairing
