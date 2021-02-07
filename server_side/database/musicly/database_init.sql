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
	password_hash varchar(64) NOT NULL,
	confirmed bool NOT NULL,
	last_login_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE liked_music (
	account_id bigint NOT NULL,
	recording_id bigint NOT NULL,
	like_status int NOT NULL
);

CREATE TABLE playlist (
	id bigserial NOT NULL,
	account_id bigint NOT NULL,
	name varchar(64)
);

CREATE TABLE playlist_music (
	playlist_id bigint NOT NULL,
	recording_id bigint NOT NULL
);

CREATE TABLE listened_to (
	account_id bigint NOT NULL,
	recording_id bigint NOT NULL,
	listen_count int NOT NULL
);

CREATE TABLE password_reset_token (
	account_id bigint NOT NULL,
	token varchar NOT NULL,
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

ALTER TABLE liked_music
	ADD CONSTRAINT account_id_fk
	FOREIGN KEY (account_id)
	REFERENCES account (id);
ALTER TABLE liked_music
	ADD CONSTRAINT recording_id_fk
	FOREIGN KEY (recording_id)
	REFERENCES recording (id);
ALTER TABLE liked_music ADD PRIMARY KEY (account_id, recording_id);
		
ALTER TABLE listened_to
	ADD CONSTRAINT account_id_fk
	FOREIGN KEY (account_id)
	REFERENCES account (id);
ALTER TABLE listened_to
	ADD CONSTRAINT recording_id_fk
	FOREIGN KEY (recording_id)
	REFERENCES recording (id);
ALTER TABLE listened_to ADD PRIMARY KEY (account_id, recording_id);

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

ALTER TABLE listened_to
	ADD CONSTRAINT positive_listen_count
	CHECK (listen_count > 0);



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