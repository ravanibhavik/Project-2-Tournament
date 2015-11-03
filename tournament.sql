-- Create Database. Drop database if already exist so that we can rerun this file
-- without any error.
drop database if exists tournament;
create database tournament;

-- Connect to newly created database tournament
\c tournament;

-- Create players table for player id and name

create table players
(id serial primary key, player_name varchar(30));

-- Create matches table for no of matches played, won, lost
-- and total points earned by player

create table matches
(id integer REFERENCES players(id) UNIQUE, matches_played int, wins int, losses int, points int);

\q


