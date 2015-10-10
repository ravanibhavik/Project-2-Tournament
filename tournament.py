#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("update tournament "
                    "set matches_played = 0, "
                    "wins = 0, "
                    "losses = 0, "
                    "points = 0")
        conn.commit()

    except psycopg2.DatabaseError as de:
        print("Database Error: " + str(de))

    finally:
        conn.close()



def deletePlayers():
    """Remove all the player records from the database."""
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("delete from tournament")
        conn.commit()

    except psycopg2.DatabaseError as de:
        print("Database Error: " + str(de))

    finally:
        conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    try:
        conn = connect()
        cur = conn.cursor()
        sql = "select count(*) from tournament"
        cur.execute(sql)
        player_count = cur.fetchone()
        conn.commit()

    except psycopg2.DatabaseError as e:
        print("Database Error: " + str(e))

    finally:
        conn.close()

    return player_count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    try:
        conn = connect()
        cur = conn.cursor()
        sql = "insert into tournament (player_name, matches_played, wins, losses, points)" \
              "values (%s , 0, 0, 0, 0)"
        cur.execute(sql, (name,))
        conn.commit()

    except psycopg2.DatabaseError as e:
        print("Database Error: " + str(e))

    finally:
        conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    try:
        conn = connect()
        cur = conn.cursor()
        sql = "select id, player_name, wins, matches_played " \
              "from tournament " \
              "order by wins desc"
        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()

    except psycopg2.DatabaseError as de:
        print("Database Error: " + str(de))

    finally:
        conn.close()

    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    try:
        conn = connect()
        cur = conn.cursor()
        sql = "update tournament " \
              "set matches_played = matches_played + 1, " \
              "wins = wins + 1, "  \
              "points = points + 3" \
              "where id = %s"
        cur.execute(sql, (winner,))
        sql = "update tournament " \
              "set matches_played = matches_played + 1, " \
              "losses = losses + 1" \
              "where id = %s"
        cur.execute(sql, (loser,))
        conn.commit()

    except psycopg2.DatabaseError as e:
        print("Database Error: " + str(e))

    finally:
        conn.close()

 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    try:
        conn = connect()
        cur = conn.cursor()
        sql = "select id, player_name from " \
              "tournament order by wins desc"
        cur.execute(sql)
        sql_result = cur.fetchall()
        len_result = len(sql_result)
        pairs = []
        for index in range(len_result):
            if index % 2 == 0:
                pairs.append(sql_result[index] + sql_result[index + 1])

    except psycopg2.DatabaseError as de:
        print("Database Error: " + de)

    finally:
        conn.close()

    return pairs
