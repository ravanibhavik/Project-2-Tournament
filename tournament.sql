-- Create Database. Drop database if already exist so file can be used rerun.
drop database if exists tournament;
create database tournament;

-- Connect to Database
\c tournament;

-- Create Tournament table which holds information like player name, no of matches played,
-- matches won, lost and points earned (considering 3 points per match won)

create table tournament
(id serial primary key, player_name varchar(30), matches_played int,
wins int, losses int, points int);


