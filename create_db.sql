drop table if exists perform;
drop table if exists artists;
drop table if exists plinclude;
drop table if exists playlists;
drop table if exists listen;
drop table if exists sessions;
drop table if exists songs;
drop table if exists users;

PRAGMA foreign_keys = ON;

create table users (
  uid		char(4),
  name		text,
  pwd		text,
  primary key (uid)
);
create table songs (
  sid		int,
  title		text,
  duration	int,
  primary key (sid)
);
create table sessions (
  uid		char(4),
  sno		int,
  start 	date,
  end 		date,
  primary key (uid,sno),
  foreign key (uid) references users
	on delete cascade
);
create table listen (
  uid		char(4),
  sno		int,
  sid		int,
  cnt		real,
  primary key (uid,sno,sid),
  foreign key (uid,sno) references sessions,
  foreign key (sid) references songs
);
create table playlists (
  pid		int,
  title		text,
  uid		char(4),
  primary key (pid),
  foreign key (uid) references users
);
create table plinclude (
  pid		int,
  sid		int,
  sorder	int,
  primary key (pid,sid),
  foreign key (pid) references playlists,
  foreign key (sid) references songs
);
create table artists (
  aid		char(4),
  name		text,
  nationality	text,
  pwd		text,
  primary key (aid)
);
create table perform (
  aid		char(4),
  sid		int,
  primary key (aid,sid),
  foreign key (aid) references artists,
  foreign key (sid) references songs
);


-- Data prepapred by Davood Rafiei, drafiei@ualberta.ca
-- Published on Sept 27, 2022
-- Data edited by Nam Son Pham, npham@ualberta.ca
-- Published on Oct 24, 2022

-- Let's insert some tuples to our tables. This is just an initial set and 
-- we definitly need more data for testing our queries.

-- Data prepapred by John Mabanta, mabanta@ualberta.ca, and published on Oct 3, 2022

PRAGMA foreign_keys = ON;

--------
-- USERS (names randomly generated)
--------


INSERT INTO users VALUES ('u01', 'Jess Beil', 'u01');
INSERT INTO users VALUES ('u02', 'Theon Solomon', 'u02');
INSERT INTO users VALUES ('u03', 'Sullivan Moses', 'u03');
INSERT INTO users VALUES ('u04', 'Rees Downling', 'u04');
INSERT INTO users VALUES ('u05', 'Zakir Cline', 'u05');
INSERT INTO users VALUES ('u06', 'Siyana Rossi', 'u06');
INSERT INTO users VALUES ('u07', 'Woodrow Hines', 'u07');
INSERT INTO users VALUES ('u08', 'Zaynab Thrope', 'u08');
INSERT INTO users VALUES ('u09', 'Tasnia Workman', 'u09');
INSERT INTO users VALUES ('u10', 'Rahima Dickinson', 'u10');

----------
-- ARTISTS
----------
INSERT INTO artists VALUES ('a01', 'Drake', 'Canada', 'a01');
INSERT INTO artists VALUES ('a02', 'Celine Dion', 'Canadian', 'a02');
INSERT INTO artists VALUES ('a03', 'Avril Lavigne', 'caNaDa', 'a03');
INSERT INTO artists VALUES ('a04', 'Rush', 'CAnaDIAN', 'a04');
INSERT INTO artists VALUES ('a05', 'The Beatles', 'British', 'a05');
INSERT INTO artists VALUES ('a06', 'Jimi Hendrix', 'American', 'a06');
INSERT INTO artists VALUES ('a07', 'PSY', 'Korean', 'a07');
INSERT INTO artists VALUES ('a08', 'Michael Jackson', 'USA', 'a08');
INSERT INTO artists VALUES ('a09', 'Pink Floyd', 'United Kingdom', 'a09');
INSERT INTO artists VALUES ('a10', 'Paul McCartney', 'UK', 'a10');

--------
-- SONGS
--------
-- Drake Songs
INSERT INTO songs VALUES (0, 'God''s Plan', 198);
INSERT INTO songs VALUES (1, 'One Dance', 173);
INSERT INTO songs VALUES (2, 'Hotline Bling', 267);
-- Celine Dion Songs
INSERT INTO songs VALUES (3, 'My Heart Will Go On', 280);
INSERT INTO songs VALUES (4, 'The Power of Love', 342);
INSERT INTO songs VALUES (5, 'Because You Loved Me', 273);
-- Avril Lavigne Songs
INSERT INTO songs VALUES (6, 'Complicated', 244);
INSERT INTO songs VALUES (7, 'Sk8er Boi', 204);
INSERT INTO songs VALUES (8, 'Girlfriend', 216);
-- Rush Songs
INSERT INTO songs VALUES (9, 'Tom Sawyer', 276);
INSERT INTO songs VALUES (10, 'Limelight', 259);
INSERT INTO songs VALUES (11, 'The Spirit of Radio', 299);
-- Beatles Songs
INSERT INTO songs VALUES (12, 'I Am The Walrus', 275);
INSERT INTO songs VALUES (13, 'Why Don''t We Do It In The Road?', 101);
INSERT INTO songs VALUES (14, 'Everybody''s Got Something To Hide Except Me And My Monkey', 144);
-- Jimi Hendrix Songs
INSERT INTO songs VALUES (15, 'Purple Haze', 170);
INSERT INTO songs VALUES (16, 'All Along the Watchtower', 240);
INSERT INTO songs VALUES (17, 'Hey Joe', 210);
-- PSY Songs
INSERT INTO songs VALUES (18, 'Gangnam Style', 219);
INSERT INTO songs VALUES (19, 'Gentleman', 194);
INSERT INTO songs VALUES (20, 'That That', 174);
-- Michael Jackson Songs
INSERT INTO songs VALUES (21, 'This Girl is Mine', 293); -- Alongside Paul McCartney
INSERT INTO songs VALUES (22, 'Off the Wall', 246);
INSERT INTO songs VALUES (23, 'Man in the Mirror', 318);
INSERT INTO songs VALUES (24, 'Who Is It', 393);
INSERT INTO songs VALUES (25, 'You Rock My World', 337);
INSERT INTO songs VALUES (26, 'Don''t Matter To Me', 245); -- Alongside Drake
-- Pink Floyd Songs
INSERT INTO songs VALUES (27, 'Dogs', 1026);
INSERT INTO songs VALUES (28, 'Us and Them', 469);
INSERT INTO songs VALUES (29, 'Comfortably Numb', 382);
-- Paul McCartney Songs
INSERT INTO songs VALUES (30, 'Maybe I''m Amazed', 229);
INSERT INTO songs VALUES (31, 'Live and Let Die', 192);
-- 'Band on the Run' has NO listeners, and NOT IN ANY PLAYLIST
-- (though the song is a banger)
INSERT INTO songs VALUES (32, 'Band on the Run', 313);

----------
-- PERFORM
----------
-- Drake Songs
INSERT INTO perform VALUES ('a01', 0);
INSERT INTO perform VALUES ('a01', 1);
INSERT INTO perform VALUES ('a01', 2);
-- Celine Dion Songs
INSERT INTO perform VALUES ('a02', 3);
INSERT INTO perform VALUES ('a02', 4);
INSERT INTO perform VALUES ('a02', 5);
-- Avril Lavigne Songs
INSERT INTO perform VALUES ('a03', 6);
INSERT INTO perform VALUES ('a03', 7);
INSERT INTO perform VALUES ('a03', 8);
-- Rush Songs
INSERT INTO perform VALUES ('a04', 9);
INSERT INTO perform VALUES ('a04', 10);
INSERT INTO perform VALUES ('a04', 11);
-- Beatles Songs
INSERT INTO perform VALUES ('a05', 12);
INSERT INTO perform VALUES ('a05', 13);
INSERT INTO perform VALUES ('a05', 14);
-- Jimi Hendrix Songs
INSERT INTO perform VALUES ('a06', 15);
INSERT INTO perform VALUES ('a06', 16);
INSERT INTO perform VALUES ('a06', 17);
-- PSY Songs
INSERT INTO perform VALUES ('a07', 18);
INSERT INTO perform VALUES ('a07', 19);
INSERT INTO perform VALUES ('a07', 20);
-- Michael Jackson Songs
INSERT INTO perform VALUES ('a08', 22);
INSERT INTO perform VALUES ('a08', 23);
INSERT INTO perform VALUES ('a08', 24);
INSERT INTO perform VALUES ('a08', 25);
-- Pink Floyd Songs
INSERT INTO perform VALUES ('a09', 27);
INSERT INTO perform VALUES ('a09', 28);
INSERT INTO perform VALUES ('a09', 29);
-- Paul McCartney Songs
INSERT INTO perform VALUES ('a10', 30);
INSERT INTO perform VALUES ('a10', 31);
INSERT INTO perform VALUES ('a10', 32);
-- COLLAB SONGS (2 artists)
-- 'This Girl is Mine' by Michael Jackson & Paul McCartney
INSERT INTO perform VALUES ('a08', 21);
INSERT INTO perform VALUES ('a10', 21);
-- 'Don't Matter To Me' by Drake & Michael Jackson
INSERT INTO perform VALUES ('a01', 26);
INSERT INTO perform VALUES ('a08', 26);

------------
-- Playlists
-- (ignore the user creator as I do not use those
--  to base which songs a user listens to)
------------

-- All Songs Playlist (pid = 0) (self evident)
-- (except 'Band on the Run')
INSERT INTO playlists VALUES (0, 'All Songs', 'u01');
INSERT INTO plinclude VALUES (0, 0, 1);
INSERT INTO plinclude VALUES (0, 1, 2);
INSERT INTO plinclude VALUES (0, 2, 3);
INSERT INTO plinclude VALUES (0, 3, 4);
INSERT INTO plinclude VALUES (0, 4, 5);
INSERT INTO plinclude VALUES (0, 5, 6);
INSERT INTO plinclude VALUES (0, 6, 7);
INSERT INTO plinclude VALUES (0, 7, 8);
INSERT INTO plinclude VALUES (0, 8, 9);
INSERT INTO plinclude VALUES (0, 9, 10);
INSERT INTO plinclude VALUES (0, 10, 11);
INSERT INTO plinclude VALUES (0, 11, 12);
INSERT INTO plinclude VALUES (0, 12, 13);
INSERT INTO plinclude VALUES (0, 13, 14);
INSERT INTO plinclude VALUES (0, 14, 15);
INSERT INTO plinclude VALUES (0, 15, 16);
INSERT INTO plinclude VALUES (0, 16, 17);
INSERT INTO plinclude VALUES (0, 17, 18);
INSERT INTO plinclude VALUES (0, 18, 19);
INSERT INTO plinclude VALUES (0, 19, 20);
INSERT INTO plinclude VALUES (0, 20, 21);
INSERT INTO plinclude VALUES (0, 21, 22);
INSERT INTO plinclude VALUES (0, 22, 23);
INSERT INTO plinclude VALUES (0, 23, 24);
INSERT INTO plinclude VALUES (0, 24, 25);
INSERT INTO plinclude VALUES (0, 25, 26);
INSERT INTO plinclude VALUES (0, 26, 27);
INSERT INTO plinclude VALUES (0, 27, 28);
INSERT INTO plinclude VALUES (0, 28, 29);
INSERT INTO plinclude VALUES (0, 29, 30);
INSERT INTO plinclude VALUES (0, 30, 31);
INSERT INTO plinclude VALUES (0, 31, 32);

-- Canadian Songs Playlist (pid = 1)
-- Contains songs by Drake, Celine Dion, Avril Lavigne, Rush
INSERT INTO playlists VALUES (1, 'Canadian Songs', 'u02');
INSERT INTO plinclude VALUES (1, 0, 1);
INSERT INTO plinclude VALUES (1, 1, 2);
INSERT INTO plinclude VALUES (1, 2, 3);
INSERT INTO plinclude VALUES (1, 3, 4);
INSERT INTO plinclude VALUES (1, 26, 5);
INSERT INTO plinclude VALUES (1, 4, 6);
INSERT INTO plinclude VALUES (1, 5, 7);
INSERT INTO plinclude VALUES (1, 6, 8);
INSERT INTO plinclude VALUES (1, 7, 9);
INSERT INTO plinclude VALUES (1, 8, 10);
INSERT INTO plinclude VALUES (1, 9, 11);
INSERT INTO plinclude VALUES (1, 10, 12);
INSERT INTO plinclude VALUES (1, 11, 13);

-- British Invasion Playlist (pid = 2)
-- Contains songs by The Beatles, Pink Floyd, Paul McCartney
INSERT INTO playlists VALUES (2, 'British Invasion', 'u03');
INSERT INTO plinclude VALUES (2, 12, 1);
INSERT INTO plinclude VALUES (2, 13, 2);
INSERT INTO plinclude VALUES (2, 14, 3);
INSERT INTO plinclude VALUES (2, 21, 4);
INSERT INTO plinclude VALUES (2, 27, 5);
INSERT INTO plinclude VALUES (2, 28, 6);
INSERT INTO plinclude VALUES (2, 29, 7);
INSERT INTO plinclude VALUES (2, 30, 8);
INSERT INTO plinclude VALUES (2, 31, 9);

-- Boomer Rock Playlist (pid = 3)
-- Contains songs by The Beatles, Jimi Hendrix, Pink Floyd, Rush
INSERT INTO playlists VALUES (3, 'Boomer Rock', 'u04');
INSERT INTO plinclude VALUES (3, 9, 1);
INSERT INTO plinclude VALUES (3, 10, 2);
INSERT INTO plinclude VALUES (3, 11, 3);
INSERT INTO plinclude VALUES (3, 12, 4);
INSERT INTO plinclude VALUES (3, 13, 5);
INSERT INTO plinclude VALUES (3, 14, 6);
INSERT INTO plinclude VALUES (3, 15, 7);
INSERT INTO plinclude VALUES (3, 16, 8);
INSERT INTO plinclude VALUES (3, 17, 9);
INSERT INTO plinclude VALUES (3, 27, 10);
INSERT INTO plinclude VALUES (3, 28, 11);
INSERT INTO plinclude VALUES (3, 29, 12);

-- New Songs Playlist (pid = 4)
-- Contains songs by Drake, PSY, Avril Lavigne
INSERT INTO playlists VALUES (4, 'New Songs', 'u05');
INSERT INTO plinclude VALUES (4, 0, 1);
INSERT INTO plinclude VALUES (4, 1, 2);
INSERT INTO plinclude VALUES (4, 2, 3);
INSERT INTO plinclude VALUES (4, 26, 4);
INSERT INTO plinclude VALUES (4, 6, 5);
INSERT INTO plinclude VALUES (4, 7, 6);
INSERT INTO plinclude VALUES (4, 8, 7);
INSERT INTO plinclude VALUES (4, 18, 8);
INSERT INTO plinclude VALUES (4, 19, 9);
INSERT INTO plinclude VALUES (4, 20, 10);

-- Solo Artists Playlist (pid = 5)
-- Contains songs by Drake, Celine Dion, Avril Lavigne, Jimi Hendrix,
-- PSY, Micahel Jackson, Paul McCartney,
-- EXCLUDING ('This Girl is Mine' and 'Don't Matter To Me')
INSERT INTO playlists VALUES (5, 'Solo Artists', 'u06');
INSERT INTO plinclude VALUES (5, 0, 1);
INSERT INTO plinclude VALUES (5, 1, 2);
INSERT INTO plinclude VALUES (5, 2, 3);
INSERT INTO plinclude VALUES (5, 3, 4);
INSERT INTO plinclude VALUES (5, 4, 5);
INSERT INTO plinclude VALUES (5, 5, 6);
INSERT INTO plinclude VALUES (5, 6, 7);
INSERT INTO plinclude VALUES (5, 7, 8);
INSERT INTO plinclude VALUES (5, 8, 9);
INSERT INTO plinclude VALUES (5, 15, 10);
INSERT INTO plinclude VALUES (5, 16, 11);
INSERT INTO plinclude VALUES (5, 17, 12);
INSERT INTO plinclude VALUES (5, 18, 13);
INSERT INTO plinclude VALUES (5, 19, 14);
INSERT INTO plinclude VALUES (5, 20, 15);
INSERT INTO plinclude VALUES (5, 22, 16);
INSERT INTO plinclude VALUES (5, 23, 17);
INSERT INTO plinclude VALUES (5, 24, 18);
INSERT INTO plinclude VALUES (5, 25, 19);
INSERT INTO plinclude VALUES (5, 30, 20);
INSERT INTO plinclude VALUES (5, 31, 21);

-- Songs by Bands Playlist (pid = 6)
-- Contains songs by Rush, The Beatles, Pink Floyd
INSERT INTO playlists VALUES (6, 'Songs by Bands', 'u07');
INSERT INTO plinclude VALUES (6, 9, 1);
INSERT INTO plinclude VALUES (6, 10, 2);
INSERT INTO plinclude VALUES (6, 11, 3);
INSERT INTO plinclude VALUES (6, 12, 4);
INSERT INTO plinclude VALUES (6, 13, 5);
INSERT INTO plinclude VALUES (6, 14, 6);
INSERT INTO plinclude VALUES (6, 27, 7);
INSERT INTO plinclude VALUES (6, 28, 8);
INSERT INTO plinclude VALUES (6, 29, 9);

-- Female Artists Playlist (pid = 7)
-- Contains songs by Celine Dion and Avril Lavigne
INSERT INTO playlists VALUES (7, 'Female Artists', 'u08');
INSERT INTO plinclude VALUES (7, 3, 1);
INSERT INTO plinclude VALUES (7, 4, 2);
INSERT INTO plinclude VALUES (7, 5, 3);
INSERT INTO plinclude VALUES (7, 6, 4);
INSERT INTO plinclude VALUES (7, 7, 5);
INSERT INTO plinclude VALUES (7, 8, 6);

-- All American Playlist (pid = 8)
-- Contains songs by Jimi Hendrix and Michael Jackson
INSERT INTO playlists VALUES (8, 'All American', 'u09');
INSERT INTO plinclude VALUES (8, 15, 1);
INSERT INTO plinclude VALUES (8, 16, 2);
INSERT INTO plinclude VALUES (8, 17, 3);
INSERT INTO plinclude VALUES (8, 21, 4);
INSERT INTO plinclude VALUES (8, 22, 5);
INSERT INTO plinclude VALUES (8, 23, 6);
INSERT INTO plinclude VALUES (8, 24, 7);
INSERT INTO plinclude VALUES (8, 25, 8);
INSERT INTO plinclude VALUES (8, 26, 9);

-- One of Each Artist Playlist (pid = 9)
-- Contains the first song inserted for each artist
INSERT INTO playlists VALUES (9, 'One of Each Artist', 'u10');
INSERT INTO plinclude VALUES (9, 0, 1); -- God's Plan, Drake
INSERT INTO plinclude VALUES (9, 3, 2); -- My Heart Will Go On, Celine Dion
INSERT INTO plinclude VALUES (9, 6, 3); -- Complicated, Avril Lavigne
INSERT INTO plinclude VALUES (9, 9, 4); -- Tom Sawyer, Rush
INSERT INTO plinclude VALUES (9, 12, 5); -- I Am The Walrus, The Beatles
INSERT INTO plinclude VALUES (9, 15, 6); -- Purple Haze, Jimi Hendrix
INSERT INTO plinclude VALUES (9, 18, 7); -- Gangnam Style, PSY
INSERT INTO plinclude VALUES (9, 22, 8); -- Off the Wall, Michael Jackson
INSERT INTO plinclude VALUES (9, 27, 9); -- Dogs, Pink Floyd
INSERT INTO plinclude VALUES (9, 30, 10); -- Maybe I'm Amazed, Paul McCartney

-----------
-- Sessions & Listen
----------

---------------------------------------------------------------------------------------------------
-- Top (5) Artists | Most Popular Song (# of Unique SONG Listeners) | # of Unique ARTIST Listeners:
  -- a02 - Celine Dion | 3 - My Heart Will Go On (6) | 7
  -- a01 - Drake | 0 - God's Plan (6) | 6
  -- a08 - Michael Jackson | 22 - Off the Wall (4) | 6
  -- a03 - Avril Lavigne | 6 - Complicated (4) | 5
  -- a06 - Jimi Hendrix | 15 - Purple Haze (4) | 4
---------------------------------------------------------------------------------------------------

---------------------------------------------------------
-- Top Artists of Each User (from most -> least listened)
-- * indicates user has listened to > 5 DIFFERENT songs
-- u01*:
  -- a09 (Pink Floyd)
  -- a08 (Michael Jackson)
  -- a02 (Celine Dion)
  -- a01 (Drake)
  -- a04 (Rush)
  -- a10 (Paul McCartney)
  -- a03 (Avril Lavigne)
  -- a06 (Jimi Hendrix)
  -- a07 (PSY)
  -- a05 (The Beatles)
-- u02:
  -- a01 (Drake)
  -- a08 (Michael Jackson)
-- u03:
  -- a02 (Celine Dion)
  -- a01 (Drake)
-- u04:
  -- a02 (Celine Dion)
  -- a01 (Drake)
  -- a03 (Avril Lavigne)
-- u05*:
  -- a05 (The Beatles)
  -- a08 (Michael Jackson)
  -- a07 (PSY)
  -- a10 (Paul McCartney)
  -- a06 (Jimi Hendrix)
  -- a02 (Celine Dion)
  -- a04 (Rush)
  -- a09 (Pink Floyd)
  -- a01 (Drake)
  -- a03 (Avril Lavigne)
-- u06:
  -- a08 (Michael Jackson)
  -- a02 (Celine Dion)
  -- a01 (Drake)
-- u07* (Also the only user that has NOT listened to a Canadian artist):
  -- a08 (Michael Jackson)
  -- a06 (Jimi Hendrix)
  -- a10 (Paul McCartney)
-- u08*:
  -- a02 (Celine Dion)
  -- a03 (Avril Lavigne)
-- u09:
  -- a02 (Celine Dion)
  -- a08 (Michael Jackson)
  -- a03 (Avril Lavinge)
  -- a06 (Jimi Hendrix)
---------------------------------------------------------

-------------------------------------------------------------------
-- Top 3 Songs For Each Month (# of Unique Listeners IN that month)
-- (in fact, the top 3 have 2 unique listeners, the rest have only 1)
-- 2022-01:
  -- 26 - 'Don't Matter To Me' (2)
  -- 0 - 'God's Plan' (2)
  -- 2 - 'One Dance' (2)
-- 2022-02:
  -- 0 - 'God's Plan' (2)
  -- 3 - 'My Heart Will Go On' (2)
  -- 4 - 'The Power of Love' (2)
-- 2022-03:
  -- 22 - 'Off the Wall' (2)
  -- 0 - 'God's Plan' (2)
  -- 3 - 'My Heart Will Go On' (2)
-- 2022-04:
  -- 15 - 'Purple Haze' (2)
  -- 7 - 'Sk8er Boi' (2)
  -- 5 - 'Because You Loved Me' (2)
-------------------------------------------------------------------

-- u01 has listened to ALL SONGS EXACTLY ONCE (cnt = 1.0) in
-- one session, EXCEPT for 'Band on the Run' (sid = 32).
INSERT INTO sessions VALUES ('u01', 1, '2022-01-01', '2022-01-02');
INSERT INTO listen VALUES ('u01', 1, 0, 1.0);
INSERT INTO listen VALUES ('u01', 1, 1, 1.0);
INSERT INTO listen VALUES ('u01', 1, 2, 1.0);
INSERT INTO listen VALUES ('u01', 1, 3, 1.0);
INSERT INTO listen VALUES ('u01', 1, 4, 1.0);
INSERT INTO listen VALUES ('u01', 1, 5, 1.0);
INSERT INTO listen VALUES ('u01', 1, 6, 1.0);
INSERT INTO listen VALUES ('u01', 1, 7, 1.0);
INSERT INTO listen VALUES ('u01', 1, 8, 1.0);
INSERT INTO listen VALUES ('u01', 1, 9, 1.0);
INSERT INTO listen VALUES ('u01', 1, 10, 1.0);
INSERT INTO listen VALUES ('u01', 1, 11, 1.0);
INSERT INTO listen VALUES ('u01', 1, 12, 1.0);
INSERT INTO listen VALUES ('u01', 1, 13, 1.0);
INSERT INTO listen VALUES ('u01', 1, 14, 1.0);
INSERT INTO listen VALUES ('u01', 1, 15, 1.0);
INSERT INTO listen VALUES ('u01', 1, 16, 1.0);
INSERT INTO listen VALUES ('u01', 1, 17, 1.0);
INSERT INTO listen VALUES ('u01', 1, 18, 1.0);
INSERT INTO listen VALUES ('u01', 1, 19, 1.0);
INSERT INTO listen VALUES ('u01', 1, 20, 1.0);
INSERT INTO listen VALUES ('u01', 1, 21, 1.0);
INSERT INTO listen VALUES ('u01', 1, 22, 1.0);
INSERT INTO listen VALUES ('u01', 1, 23, 1.0);
INSERT INTO listen VALUES ('u01', 1, 24, 1.0);
INSERT INTO listen VALUES ('u01', 1, 25, 1.0);
INSERT INTO listen VALUES ('u01', 1, 26, 1.0);
INSERT INTO listen VALUES ('u01', 1, 27, 1.0);
INSERT INTO listen VALUES ('u01', 1, 28, 1.0);
INSERT INTO listen VALUES ('u01', 1, 29, 1.0);
INSERT INTO listen VALUES ('u01', 1, 30, 1.0);
INSERT INTO listen VALUES ('u01', 1, 31, 1.0);
-- INSERT INTO listen VALUES ('u01', 1, 32, 1.0);

-- u02 has ONLY LISTENED to Drake (+ his collab with MJ),
-- split between two sessions
INSERT INTO sessions VALUES ('u02', 1, '2022-01-06', '2022-01-07');
INSERT INTO sessions VALUES ('u02', 2, '2022-02-15', '2022-02-16');
INSERT INTO listen VALUES ('u02', 1, 0, 2.4);
INSERT INTO listen VALUES ('u02', 1, 2, 0.9);
INSERT INTO listen VALUES ('u02', 1, 26, 1.2);
INSERT INTO listen VALUES ('u02', 2, 1, 3.7);
INSERT INTO listen VALUES ('u02', 2, 2, 0.1);

-- u03 has listened to Drake and Celine Dion
INSERT INTO sessions VALUES ('u03', 1, '2022-02-26', '2022-02-27');
INSERT INTO listen VALUES ('u03', 1, 3, 2.3);
INSERT INTO listen VALUES ('u03', 1, 0, 3.2);
INSERT INTO listen VALUES ('u03', 1, 4, 1.9);

-- u04 has listened to Drake and Celine Dion and Avril Lavigne
INSERT INTO sessions VALUES ('u04', 1, '2022-02-14', '2022-02-15');
INSERT INTO listen VALUES ('u04', 1, 0, 5.2);
INSERT INTO listen VALUES ('u04', 1, 3, 2.1);
INSERT INTO listen VALUES ('u04', 1, 4, 3.3);
INSERT INTO listen VALUES ('u04', 1, 5, 1.0);
INSERT INTO listen VALUES ('u04', 1, 6, 1.4);

-- u05 listens to one of each artist (SAME SONGS as playlist)
-- split between 3 sessions all in the same month
INSERT INTO sessions VALUES ('u05', 1, '2022-03-01', '2022-03-02');
INSERT INTO sessions VALUES ('u05', 2, '2022-03-03', '2022-03-02');
INSERT INTO sessions VALUES ('u05', 3, '2022-03-01', '2022-03-02');
INSERT INTO listen VALUES ('u05', 1, 0, 1.2);
INSERT INTO listen VALUES ('u05', 1, 3, 2.3);
INSERT INTO listen VALUES ('u05', 1, 6, 0.2);
INSERT INTO listen VALUES ('u05', 2, 9, 2.0);
INSERT INTO listen VALUES ('u05', 2, 12, 10.9);
INSERT INTO listen VALUES ('u05', 2, 15, 4.3);
INSERT INTO listen VALUES ('u05', 3, 18, 12.1);
INSERT INTO listen VALUES ('u05', 3, 22, 11.2);
INSERT INTO listen VALUES ('u05', 3, 27, 0.5);
INSERT INTO listen VALUES ('u05', 3, 30, 6.9);

-- u06 listens to Drake, Celine Dion, and Michael Jackson
INSERT INTO sessions VALUES ('u06', 1, '2022-03-24', '2022-03-25');
INSERT INTO listen VALUES ('u06', 1, 0, 2.3);
INSERT INTO listen VALUES ('u06', 1, 3, 3.8);
INSERT INTO listen VALUES ('u06', 1, 22, 7.9);

-- u07 listenes to the All American Playlist
-- (except 23 - 'Man in the Mirror', 26 - 'Don't Matter To Me')
INSERT INTO sessions VALUES ('u07', 1, '2022-04-12', '2022-04-13');
INSERT INTO listen VALUES ('u07', 1, 15, 3.2);
INSERT INTO listen VALUES ('u07', 1, 16, 2.9);
INSERT INTO listen VALUES ('u07', 1, 17, 4.2);
INSERT INTO listen VALUES ('u07', 1, 21, 2.5);
INSERT INTO listen VALUES ('u07', 1, 22, 1.01);
INSERT INTO listen VALUES ('u07', 1, 24, 1.21);
INSERT INTO listen VALUES ('u07', 1, 25, 3.14);

-- u08 listens to the Female Artists Playlist
INSERT INTO sessions VALUES ('u08', 1, '2022-04-15', '2022-04-16');
INSERT INTO listen VALUES ('u08', 1, 3, 1.0004);
INSERT INTO listen VALUES ('u08', 1, 4, 2.3);
INSERT INTO listen VALUES ('u08', 1, 5, 5.2);
INSERT INTO listen VALUES ('u08', 1, 6, 1.2);
INSERT INTO listen VALUES ('u08', 1, 7, 0.9);
INSERT INTO listen VALUES ('u08', 1, 8, 4.4);

-- u09 listens to 'Purple Haze' (Jimi Hendrix), 'Man in the Mirror' (Michael Jackson)
-- 'Sk8er Boi' (Avril Lavigne), and 'Because You Loved Me' (Celine Dion)
INSERT INTO sessions VALUES ('u09', 1, '2022-04-29', '2022-04-30');
INSERT INTO listen VALUES ('u09', 1, 15, 2.3);
INSERT INTO listen VALUES ('u09', 1, 23, 5.55);
INSERT INTO listen VALUES ('u09', 1, 7, 2.376);
INSERT INTO listen VALUES ('u09', 1, 5, 7.77);
