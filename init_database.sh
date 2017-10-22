#!/bin/sh

if [ -z ${DATABASE_NAME} ]; then
    echo "Database configuration unavailable!"
    echo "Ensure .env is setup properly and this script is run from the virtualenv"
    exit 1
fi

echo -n "Loading user and database...\n(mysql) "
sudo mysql -u root -p <<ENDSQL
CREATE DATABASE ${DATABASE_NAME} CHARACTER SET utf8 COLLATE utf8_bin;
CREATE USER '${DATABASE_USERNAME}'@'${DATABASE_HOST}' IDENTIFIED BY '${DATABASE_PASSWORD}';
GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${DATABASE_USERNAME}'@'${DATABASE_HOST}';
FLUSH PRIVILEGES;
ENDSQL

echo -n "Generating option file..."
cat <<ENDCNF > db.cnf
[client]
host = ${DATABASE_HOST}
database = ${DATABASE_NAME}
user = ${DATABASE_USERNAME}
password = ${DATABASE_PASSWORD}
default-character-set = utf8
ENDCNF
echo " OK"

echo -n "Loading tables..."
mysql --defaults-extra-file=db.cnf < schema.sql
echo " OK"
