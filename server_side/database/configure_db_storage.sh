echo "echo 'SHOW data_directory;' | psql" | sudo su - postgres

sudo systemctl stop postgresql
sudo rsync -av /var/lib/postgresql /storage/
sudo mv /var/lib/postgresql/13/main /var/lib/postgresql_backup

sudo sed -Ei.bak "s|(data_directory = ')(.*)(/postgresql.*)|\1/storage\3|" /etc/postgresql/13/main/postgresql.conf
sudo sed -Ei.bak "/^local   all             postgres.*/a local   all             all                                     md5" /etc/postgresql/13/main/pg_hba.conf

sudo systemctl start postgresql
sudo systemctl status postgresql
