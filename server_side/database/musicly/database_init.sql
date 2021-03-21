/*===========================================*/
/*             MUSIC DATA TABLES             */
/*===========================================*/
CREATE TABLE musicly_recording (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	length int
);

CREATE TABLE musicly_artist (
	id bigserial NOT NULL,
	stage_name varchar NOT NULL
);

CREATE TABLE musicly_performed (
	recording_id bigint NOT NULL,
	artist_id bigint NOT NULL
);

/*===========================================*/
/*                CONSTRAINTS                */
/*===========================================*/
ALTER TABLE musicly_recording ADD PRIMARY KEY (id);
ALTER TABLE musicly_artist ADD PRIMARY KEY (id);

ALTER TABLE musicly_performed
	ADD CONSTRAINT recording_fk
	FOREIGN KEY (recording_id)
	REFERENCES musicly_recording (id);
ALTER TABLE musicly_performed
	ADD CONSTRAINT artist_fk
	FOREIGN KEY (artist_id)
	REFERENCES musicly_artist (id);
ALTER TABLE musicly_performed
	ADD CONSTRAINT unique_performer
	UNIQUE (recording_id, artist_id);

ALTER TABLE musicly_recording
	ADD CONSTRAINT positive_length
	CHECK (length >= 0);

/*===========================================*/
/*                  INDEXES                  */
/*===========================================*/
CREATE INDEX title_index ON musicly_recording (title NULLS LAST);
CREATE INDEX artist_index ON musicly_artist (stage_name);
CREATE INDEX performed_artist_index ON musicly_performed (artist_id);
CREATE INDEX performed_recording_index ON musicly_performed (recording_id);


/*===========================================*/
/*                IMPORT DATA                */
/*===========================================*/
INSERT INTO musicly_artist(stage_name) SELECT name FROM artist_dump ORDER BY id;
INSERT INTO musicly_recording(title, length) SELECT title, length FROM recording_dump ORDER BY id;
INSERT INTO musicly_performed(recording_id, artist_id) SELECT recording_id, artist_id FROM performed_dump;


/*===========================================*/
/*           DROP TEMPORARY TABLES           */
/*===========================================*/
DROP TABLE performed_dump;
DROP TABLE recording_dump;
DROP TABLE artist_dump;
