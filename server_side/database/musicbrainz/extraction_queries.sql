/*---------------------------------------------------------------*/
/*					  DROP TABLES IF EXIST						 */
/*---------------------------------------------------------------*/

DROP TABLE IF EXISTS public.recording_dump;
DROP TABLE IF EXISTS public.artist_dump;
DROP TABLE IF EXISTS public.performed_dump;

/*---------------------------------------------------------------*/
/*					 CREATE TABLES FOR DUMP						 */
/*---------------------------------------------------------------*/

CREATE TABLE public.recording_dump (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	length int,
	old_id bigint NOT NULL
);

CREATE TABLE public.artist_dump (
	id bigserial NOT NULL,
	name varchar NOT NULL,
	old_id bigint NOT NULL
);

CREATE TABLE public.performed_dump (
	recording_id bigint NOT NULL,
	artist_id bigint NOT NULL
);

/*---------------------------------------------------------------*/
/*					  EXTRACT RELEVANT DATA						 */
/*---------------------------------------------------------------*/

INSERT INTO public.recording_dump(title, length, old_id)
	SELECT name, length, id
	FROM musicbrainz.recording
	ORDER BY id;

INSERT INTO public.artist_dump(name, old_id)
	SELECT name, id
	FROM musicbrainz.artist
	ORDER BY id;

INSERT INTO public.performed_dump(recording_id, artist_id)
	SELECT recording_dump.id, artist_dump.id
	FROM public.recording_dump
	JOIN musicbrainz.recording ON (recording.id = recording_dump.old_id)
	JOIN musicbrainz.artist_credit ON (artist_credit.id = recording.artist_credit)
	JOIN musicbrainz.artist_credit_name ON (artist_credit_name.artist_credit = artist_credit.id)
	JOIN musicbrainz.artist ON (artist_credit_name.artist = artist.id)
	JOIN public.artist_dump ON (artist_dump.old_id = artist.id)
	GROUP BY recording_dump.id, artist_dump.id;

/*---------------------------------------------------------------*/