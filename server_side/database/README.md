# Postgres configuration
Use the `configure_db_storage.sh` script to configure postgres service. It will set data directory (where the data is actually stored) to `/storage/` directory on your system. And change the socket settings so you can authernticate to `psql` with users' passwords from localhost.


# Musicly database setup
Running the `database_setup.sh` script will create and configure the Musicly database so it can be used with no further actions required. Note: this assumes that the `configure_db_storage.sh` script has been run before and Musicbrainz database has been localy configured after that.

What it does is as follows:
* create `musicly` database and `db_admin` user
* extracts relevant data from `musicbrainz` database into separate tables 
* dumps the data from prepared tables and streams the output back to `psql` to insert it to `musicly` database
* create data structures in the new database, migrate data from imported 'temporary' tables that are being removed after that
* moves the data to `musicly` schema
* grants privileges on `musicly` database and its objects to db_admin user


```
sudo ./configure_db_storage.sh
# prepare local copy of Musicbrainz database here
sudo ./database_setup.sh
echo "Everything should work just fine now. Enjoy :)"
```