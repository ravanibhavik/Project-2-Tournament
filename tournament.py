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
        cur.execute("UPDATE MATCHES "
                    "SET MATCHES_PLAYED = 0, "
                    "WINS = 0, "
                    "LOSSES = 0, "
                    "POINTS = 0")
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
        cur.execute("DELETE FROM MATCHES")
        cur.execute("DELETE FROM PLAYERS")
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
        sql = "SELECT COUNT(*) FROM PLAYERS"
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
        sql = "INSERT INTO PLAYERS (PLAYER_NAME)" \
              "VALUES (%s)"
        cur.execute(sql, (name,))
        sql = "SELECT ID FROM PLAYERS WHERE PLAYER_NAME = %s"
        cur.execute(sql, (name,))
        player = cur.fetchone()
        sql = "INSERT INTO MATCHES (ID, MATCHES_PLAYED, WINS, LOSSES, POINTS) " \
              "VALUES (%s, 0, 0, 0, 0)"
        cur.execute(sql, player)
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
        sql = "SELECT M.ID, P.PLAYER_NAME, M.WINS, M.MATCHES_PLAYED " \
              "FROM MATCHES AS M, PLAYERS AS P " \
              "WHERE M.ID = P.ID " \
              "ORDER BY M.WINS DESC" \

        cur.execute(sql)
        result = cur.fetchall()
        conn.commit()

    except psycopg2.DatabaseError as de:
        print("Database Error: " + str(de))
        result = (None, None, None, None)

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
        sql = "UPDATE MATCHES " \
              "SET MATCHES_PLAYED = MATCHES_PLAYED + 1, " \
              "WINS = WINS + 1, "  \
              "POINTS = POINTS + 3" \
              "WHERE ID = %s"
        cur.execute(sql, (winner,))
        sql = "UPDATE MATCHES " \
              "SET MATCHES_PLAYED = MATCHES_PLAYED + 1, " \
              "LOSSES = LOSSES + 1" \
              "WHERE ID = %s"
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
        sql = "SELECT M.ID, P.PLAYER_NAME FROM " \
              "PLAYERS AS P, MATCHES AS M " \
              "WHERE M.ID = P.ID " \
              "ORDER BY WINS DESC"
        cur.execute(sql)
        sql_result = cur.fetchall()
        len_result = len(sql_result)
        pairs = []
        for index in range(len_result):
            if index % 2 == 0:
                pairs.append(sql_result[index] + sql_result[index + 1])

    except psycopg2.DatabaseError as de:
        print("Database Error: " + de)
        pairs = []

    finally:
        conn.close()

    return pairs

if __name__ == '__main__':
    reportMatch(12, 14)
    reportMatch(13, 15)
