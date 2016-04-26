-- Table definitions for the tournament project.

CREATE DATABASE tournament;

-- Table to register players

CREATE TABLE players ( pl_id SERIAL primary key,
                       pl_name text );

--Table of matches, winners and loosers id. Round in case of developing DB.

CREATE TABLE matches ( match_id SERIAL primary key,
                       round int,
                       win_pl_id int references players (pl_id),
                       loose_pl_id int references players (pl_id) );

-- Creating view to get numbers of wins and losses

CREATE VIEW pl_wins as ( SELECT players.pl_id, players.pl_name,
                       count(matches.win_pl_id) as wins, count(matches.loose_pl_id) as loose 
                       from players left join matches on players.pl_id=matches.win_pl_id
                       group by players.pl_id )
