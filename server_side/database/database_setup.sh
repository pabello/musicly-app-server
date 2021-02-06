# Create database and a user to operate on it
echo "createuser db_admin; createdb musicly;" | sudo su - postgres

# Create data dump from MusicBrainz database and load it into Musicly database
echo "echo '$(cat musicbrainz/extraction_queries.sql)' | psql -U postgres musicbrainz" | sudo su - postgres
echo "pg_dump -U postgres -d musicbrainz -t recording_dump -t artist_dump -t performed_dump | psql -U postgres musicly" | sudo su - postgres

# Create database structures - tables for user data and for music data. Migrate data from tables imported from musicbrainz.
echo "echo '$(cat musicly/database_init.sql)' | psql -U postgres musicly" | sudo su - postgres
echo "echo 'ALTER SCHEMA public RENAME TO musicly; CREATE SCHEMA public;' | psql -U postgres musicly" | sudo su - postgres

# Grant access on Musicly db to db_admin user
echo "echo '$(cat musicly/configure_admin_privileges.sql)' | psql -U postgres musicly" | sudo su - postgres