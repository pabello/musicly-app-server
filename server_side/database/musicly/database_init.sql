/*            DATABASE ADMINISTRATION            */


/*            MUSIC DATA TABLES            */
CREATE TABLE recording (
	id bigserial NOT NULL,
	title varchar NOT NULL
);

CREATE TABLE artist (
	id bigserial NOT NULL,
	name varchar NOT NULL
);

CREATE TABLE performed (
	recording_id bigint NOT NULL,
	artist_id bigint NOT NULL
);

/*            CONSTRAINTS            */
ALTER TABLE recording ADD PRIMARY KEY (id);

ALTER TABLE artist ADD PRIMARY KEY (id);

ALTER TABLE performed
	ADD CONSTRAINT recording_fk
	FOREIGN KEY (recording_id)
	REFERENCES recording (id);

ALTER TABLE performed
	ADD CONSTRAINT artist_fk
	FOREIGN KEY (artist_id)
	REFERENCES artist (id);
	
ALTER TABLE performed
	ADD CONSTRAINT unique_performer
	UNIQUE (recording_id, artist_id);



/*            USER CONTENT TABLES            */
CREATE TABLE account (
	id bigserial NOT NULL,
	username varchar(32) NOT NULL,
	email varchar(254) NOT NULL,
	password_hash varchar(64) NOT NULL,
	confirmed bool NOT NULL,
	last_login_time timestamp
);

CREATE TABLE liked_music (
	account_id bigint NOT NULL,
	recording_id bigint NOT NULL,
	like_status int NOT NULL
);

/*            CONSTRAINTS            */
ALTER TABLE account ADD PRIMARY KEY (id);

ALTER TABLE account
	ADD CONSTRAINT unique_username
	UNIQUE (username);
	
ALTER TABLE account
	ADD CONSTRAINT unique_email
	UNIQUE (email);
	
ALTER TABLE liked_music
	ADD CONSTRAINT user_fk
	FOREIGN KEY (account_id)
	REFERENCES account (id);
	
ALTER TABLE liked_music
	ADD CONSTRAINT recording_fk
	FOREIGN KEY (recording_id)
	REFERENCES recording (id);
	
ALTER TABLE liked_music
	ADD CONSTRAINT unique_like
	UNIQUE (account_id, recording_id);



/*            IMPORT DATA            */
INSERT INTO artist(name) SELECT name FROM artist_dump ORDER BY id;
INSERT INTO recording(title) SELECT title FROM recording_dump ORDER BY id;
INSERT INTO performed(recording_id, artist_id) SELECT recording_id, artist_id FROM performed_dump;



/*       DROP TEMPORARY TABLES       */
DROP TABLE performed_dump;
DROP TABLE recording_dump;
DROP TABLE artist_dump;