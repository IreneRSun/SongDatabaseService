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
  pwd       text,
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
  pwd       text,
  primary key (aid)
);
create table perform (
  aid		char(4),
  sid		int,
  primary key (aid,sid),
  foreign key (aid) references artists,
  foreign key (sid) references songs
);

insert into users values ("admin", "admin", "admin");
insert into users values ("junye", "John Yu", "junye");
insert into users values ("test", "test", NULL);
insert into users values ("ss", "Spongebob Squarepants", "ss");
insert into users values ("ps", "Patrick Starr", "ps");

insert into songs values (0, "Baby", 2);
insert into songs values (1, "Yummy", 4);
insert into songs values (2, "Love Yourself", 4);
insert into songs values (3, "Peaches", 3);
insert into songs values (4, "Beauty And A Beat", 2);
insert into songs values (5, "Ghost", 3);
insert into songs values (6, "Jimmy Cooks", 3);
insert into songs values (7, "Feel No Ways", 3);
insert into songs values (8, "Knife Talk", 3);
insert into songs values (9, "Way 2 Sexy", 3);
insert into songs values (10, "Chicago Freestyle", 3);
insert into songs values (11, "Toosie Slide", 3);
insert into songs values (12, "Wants and Needs", 3);
insert into songs values (13, "Nonstop", 3);
insert into songs values (14, "My Heart Will Go On", 3);
insert into songs values (15, "It's All Coming Back To Me Now", 3);
insert into songs values (16, "To Love You More", 3);
insert into songs values (17, "I'm Alive", 3);
insert into songs values (18, "All By Myself", 3);
insert into songs values (19, "The Power Of Love", 3);
insert into songs values (20, "That's The Way It Is", 3);
insert into songs values (21, "Just Walk Away", 3);
insert into songs values (22, "I Surrender", 3);
insert into songs values (23, "I Love You", 3);
insert into songs values (24, "Senorita", 3);
insert into songs values (25, "I Know What You Did Last Summer", 3);
insert into songs values (26, NULL, 3);
insert into songs values (27, NULL, 3);
insert into songs values (28, NULL, 3);
insert into songs values (29, "Test1", 3);
insert into songs values (30, "Test2", 3);
insert into songs values (31, "Test3", 3);
insert into songs values (32, "Test4", NULL);
insert into songs values (33, "Test5", NULL);
insert into songs values (34, "Test6", NULL);

insert into sessions values ("admin", 0, "2022-10-23 16:01:41", "2022-10-23 17:26:32");
insert into sessions values ("admin", 1, "2022-10-23 17:27:27", "2022-10-23 17:28:28");
insert into sessions values ("admin", 2, "2022-10-23 17:36:36", NULL);
insert into sessions values ("ss", 0, "2022-10-25 14:34:08", NULL);
insert into sessions values ("ps", 0, "2022-10-25 14:36:21", NULL);

insert into listen values ("admin", 0, 0, 1);
insert into listen values ("admin", 0, 1, 1);
insert into listen values ("admin", 0, 2, 1);
insert into listen values ("admin", 0, 3, 1);
insert into listen values ("admin", 0, 4, 1);
insert into listen values ("admin", 0, 5, 1);
insert into listen values ("admin", 0, 6, 2);
insert into listen values ("admin", 0, 14, 3);
-- insert into listen values ("admin", 2, 0, 1);
insert into listen values ("ss", 0, 0, 2);
insert into listen values ("ss", 0, 6, 1);
insert into listen values ("ss", 0, 7, 1);
insert into listen values ("ss", 0, 8, 1);
insert into listen values ("ss", 0, 9, 1);
insert into listen values ("ss", 0, 10, 1);
insert into listen values ("ss", 0, 11, 1);
insert into listen values ("ss", 0, 12, 1);
insert into listen values ("ss", 0, 13, 1);
insert into listen values ("ss", 0, 14, 3);
insert into listen values ("ps", 0, 1, 2);
insert into listen values ("ps", 0, 7, 3);
insert into listen values ("ps", 0, 14, 1);
insert into listen values ("ps", 0, 15, 1);
insert into listen values ("ps", 0, 16, 1);
insert into listen values ("ps", 0, 17, 1);
insert into listen values ("ps", 0, 18, 1);
insert into listen values ("ps", 0, 19, 1);
insert into listen values ("ps", 0, 20, 1);
insert into listen values ("ps", 0, 21, 1);
insert into listen values ("ps", 0, 22, 1);
insert into listen values ("ps", 0, 23, 1);

insert into playlists values (0, "happy", "admin");
insert into playlists values (1, "sad", "admin");
insert into playlists values (2, "mad", "admin");
insert into playlists values (3, "scared", "admin");
insert into playlists values (4, "disgust", "admin");
insert into playlists values (5, NULL, "admin");
insert into playlists values (6, NULL, "admin");
insert into playlists values (7, NULL, "admin");
insert into playlists values (8, "I Luv Drake", "ss");
insert into playlists values (9, "I Luv Celine Dion", "ps");
insert into playlists values (10, Coding Vibez, NULL);
insert into playlists values (11, LIFTTTT, NULL);

insert into plinclude values (0, 0, NULL);
insert into plinclude values (0, 1, NULL);
insert into plinclude values (0, 2, NULL);
insert into plinclude values (1, 3, NULL);
insert into plinclude values (1, 4, NULL);
insert into plinclude values (1, 5, NULL);
insert into plinclude values (2, 6, NULL);
insert into plinclude values (2, 7, NULL);
insert into plinclude values (2, 8, NULL);
insert into plinclude values (2, 9, NULL);
insert into plinclude values (2, 10, NULL);
insert into plinclude values (2, 11, NULL);
insert into plinclude values (2, 12, NULL);
insert into plinclude values (2, 13, NULL);
insert into plinclude values (8, 6, 0);
insert into plinclude values (8, 7, 1);
insert into plinclude values (8, 8, 2);
insert into plinclude values (8, 9, 3);
insert into plinclude values (8, 10, 4);
insert into plinclude values (8, 11, 5);
insert into plinclude values (8, 12, 6);
insert into plinclude values (8, 13, 7);
insert into plinclude values (9, 14, 0);
insert into plinclude values (9, 15, 1);
insert into plinclude values (9, 16, 2);
insert into plinclude values (9, 17, 3);
insert into plinclude values (9, 18, 4);
insert into plinclude values (9, 19, 5);
insert into plinclude values (9, 20, 6);
insert into plinclude values (9, 21, 7);
insert into plinclude values (9, 22, 8);
insert into plinclude values (9, 23, 9);
insert into plinclude values (10, 1, 0);
insert into plinclude values (10, 7, 1);
insert into plinclude values (10, 12, 2);
insert into plinclude values (10, 14, 3);
insert into plinclude values (10, 15, 4);
insert into plinclude values (10, 16, 5);
insert into plinclude values (10, 22, 6);
insert into plinclude values (10, 33, 7);
insert into plinclude values (11, NULL, 0);
insert into plinclude values (11, NULL, 1);
insert into plinclude values (11, NULL, 2);
insert into plinclude values (11, NULL, 3);


insert into artists values ("a0", "Justin Bieber", "Canadian", "a0");
insert into artists values ("junye", "John Yu", "Canadian", "junye");
insert into artists values ("a1", "Drake", "Canadian", "a1");
insert into artists values ("a2", "Celine Dion", "Canadian", "a2");
insert into artists values ("a3", "Shania Twain", "Canadian", "a3");
insert into artists values ("a4", "Bryan Adams", "Canadian", "a4");
insert into artists values ("a5", "The Weeknd", "Canadian", "a5");
insert into artists values ("a6", "Avril Lavigne", "Canadian", "a6");
insert into artists values ("a7", "Shawn Mendes", "Canadian", "a7");
insert into artists values ("a8", "Taylor Swift", "American", "a8");
insert into artists values ("a9", "Ariana Grande", "American", "a9");
insert into artists values ("a10", "Katy Perry", "American", "a10");
insert into artists values ("a11", "Olivia Rodrigo", "American", "a11");
insert into artists values ("a12", "Billie Eilish", "American", "a12");
insert into artists values ("a13", "Miley Cyrus", "American", "a13");
insert into artists values ("a14", "Rihanna", "Barbadian", "a14");
insert into artists values ("a15", "Lady Gaga", "American", "a15");
insert into artists values ("a16", "Beyonce", "American", "a16");
insert into artists values ("a17", "Demi Lovato", "American", "a17");
insert into artists values ("a18", "Britney Spears", "American", "a18");
insert into artists values ("a19", "Camila Cabello", "American", "a19");
insert into artists values ("a20", NULL, NULL, "a20");
insert into artists values ("a21", NULL, NULL, "a21");
insert into artists values ("a22", NULL, NULL, "a22");
insert into artists values ("a23", "Test1", NULL, "a23");
insert into artists values ("a24", "DJ Snake", "American", "a24");

insert into perform values ("a0", 0);
insert into perform values ("a0", 1);
insert into perform values ("a0", 2);
insert into perform values ("a0", 3);
insert into perform values ("a0", 4);
insert into perform values ("a0", 5);
insert into perform values ("a1", 6);
insert into perform values ("a1", 7);
insert into perform values ("a1", 8);
insert into perform values ("a1", 9);
insert into perform values ("a1", 10);
insert into perform values ("a1", 11);
insert into perform values ("a1", 12);
insert into perform values ("a1", 13);
insert into perform values ("a2", 14);
insert into perform values ("a2", 15);
insert into perform values ("a2", 16);
insert into perform values ("a2", 17);
insert into perform values ("a2", 18);
insert into perform values ("a2", 19);
insert into perform values ("a2", 20);
insert into perform values ("a2", 21);
insert into perform values ("a2", 22);
insert into perform values ("a2", 23);
insert into perform values ("a7", 24);
insert into perform values ("a19", 24);
insert into perform values ("a7", 25);
insert into perform values ("a19", 25);
insert into perform values ("a20", 29);
insert into perform values ("a23", 26);
insert into perform values ("a20", 26);