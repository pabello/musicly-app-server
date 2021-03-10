/*===========================================*/
/*             MUSIC DATA TABLES             */
/*===========================================*/
CREATE TABLE recording (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	length int
);

CREATE TABLE artist (
	id bigserial NOT NULL,
	stage_name varchar NOT NULL
);

CREATE TABLE performed (
	recording_id bigint NOT NULL,
	artist_id bigint NOT NULL
);

/*===========================================*/
/*                CONSTRAINTS                */
/*===========================================*/
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

ALTER TABLE recording
	ADD CONSTRAINT positive_length
	CHECK (length >= 0);

/*===========================================*/
/*                  INDEXES                  */
/*===========================================*/
CREATE INDEX title_index ON recording (title NULLS LAST);
CREATE INDEX artist_index ON artist (stage_name);


/*===========================================*/
/*            USER CONTENT TABLES            */
/*===========================================*/
CREATE TABLE account (
	id bigserial NOT NULL,
	username varchar(32) NOT NULL,
	email varchar(254) NOT NULL,
	password char(64) NOT NULL,
	confirmed bool NOT NULL DEFAULT false,
	last_login timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_music (
   	id bigserial NOT NULL,
	account_id bigint NOT NULL,
	recording_id bigint NOT NULL,
	like_status int NOT NULL,
    	listen_count int NOT NULL
);

CREATE TABLE playlist (
	id bigserial NOT NULL,
	account_id bigint NOT NULL,
	name varchar(64),
	length int NOT NULL DEFAULT 0,
	music_count int NOT NULL DEFAULT 0
);

CREATE TABLE playlist_music (
    	id bigserial NOT NULL,
	playlist_id bigint NOT NULL,
	recording_id bigint NOT NULL,
    	playlist_position int NOT NULL
);

CREATE TABLE password_reset_token (
	account_id bigint NOT NULL,
	token varchar(64) NOT NULL,
	expires_at timestamp NOT NULL
);

/*===========================================*/
/*                CONSTRAINTS                */
/*===========================================*/
/*                TABLE KEYS                 */
ALTER TABLE account ADD PRIMARY KEY (id);

ALTER TABLE password_reset_token
	ADD CONSTRAINT account_id_fk
	FOREIGN KEY (account_id)
	REFERENCES account (id);
ALTER TABLE password_reset_token ADD PRIMARY KEY (account_id);

ALTER TABLE user_music
	ADD CONSTRAINT account_id_fk
	FOREIGN KEY (account_id)
	REFERENCES account (id);
ALTER TABLE user_music
	ADD CONSTRAINT recording_id_fk
	FOREIGN KEY (recording_id)
	REFERENCES recording (id);
ALTER TABLE user_music ADD PRIMARY KEY (id);
		
ALTER TABLE playlist
	ADD CONSTRAINT account_id_fk
	FOREIGN KEY (account_id)
	REFERENCES account (id);
ALTER TABLE playlist ADD PRIMARY KEY (id);

ALTER TABLE playlist_music
	ADD CONSTRAINT playlist_id_fk
	FOREIGN KEY (playlist_id)
	REFERENCES playlist (id);
ALTER TABLE playlist_music
	ADD CONSTRAINT recording_id_fk
	FOREIGN KEY (recording_id)
	REFERENCES recording (id);
ALTER TABLE playlist_music ADD PRIMARY KEY (id);


/*             VALUE CONSTRAINTS             */
ALTER TABLE account
	ADD CONSTRAINT unique_username
	UNIQUE (username);
	
ALTER TABLE account
	ADD CONSTRAINT unique_email
	UNIQUE (email);

ALTER TABLE password_reset_token
	ADD CONSTRAINT unique_token
	UNIQUE (token);

ALTER TABLE password_reset_token
	ADD CONSTRAINT expire_in_future
	CHECK (expires_at > CURRENT_TIMESTAMP);

ALTER TABLE user_music
	ADD CONSTRAINT positive_listen_count
	CHECK (listen_count >= 0);

ALTER TABLE playlist_music
	ADD CONSTRAINT positive_playlist_position
	CHECK (playlist_position >= 0);

ALTER TABLE playlist
	ADD CONSTRAINT positive_length
	CHECK (length >= 0);

ALTER TABLE playlist
	ADD CONSTRAINT positive_music_count
	CHECK (music_count >= 0);



/*===========================================*/
/*                IMPORT DATA                */
/*===========================================*/
INSERT INTO artist(stage_name) SELECT name FROM artist_dump ORDER BY id;
INSERT INTO recording(title, length) SELECT title, length FROM recording_dump ORDER BY id;
INSERT INTO performed(recording_id, artist_id) SELECT recording_id, artist_id FROM performed_dump;



/*===========================================*/
/*           DROP TEMPORARY TABLES           */
/*===========================================*/
DROP TABLE performed_dump;
DROP TABLE recording_dump;
DROP TABLE artist_dump;
