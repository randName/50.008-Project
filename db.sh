#!/bin/sh

DB_OPT="--defaults-extra-file=${DJANGO_DATABASE_OPTIONS}"

usage() {
	echo "usage: $0 <command>"
	echo
	echo "available commands:"
	echo "    init    create new user and db, generate option file, migrate, load schema"
	echo "    drop    drop db and user"
	echo "    reset   drop then recreate db, migrate, load schema"
	exit 1
}

create_user() {
	echo -n "Creating user…\n(mysql) "
	sudo mysql -u root -p <<-ENDSQL
	CREATE USER '${DATABASE_USERNAME}'@'${DATABASE_HOST}' IDENTIFIED BY '${DATABASE_PASSWORD}';
	GRANT ALL ON *.* TO '${DATABASE_USERNAME}'@'${DATABASE_HOST}';
	SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES';
	FLUSH PRIVILEGES;
	ENDSQL
}

drop_user() {
	echo -n "Dropping user…\n(mysql) "
	echo "DROP USER '${DATABASE_USERNAME}'@'${DATABASE_HOST}';" | sudo mysql -u root -p
}

create_db() {
	echo -n "Creating database…"
	echo "CREATE DATABASE ${DATABASE_NAME} CHARACTER SET utf8 COLLATE utf8_bin;" | mysql ${DB_OPT} --database=information_schema
	echo " OK"
}

drop_db() {
	echo -n "Dropping database…"
	echo "DROP DATABASE ${DATABASE_NAME};" | mysql ${DB_OPT}
	echo " OK"
}

gen_cnf() {
	echo -n "Generating option file…"
	cat <<-ENDCNF > ${DJANGO_DATABASE_OPTIONS}
	[client]
	host = ${DATABASE_HOST}
	user = ${DATABASE_USERNAME}
	password = ${DATABASE_PASSWORD}
	database = ${DATABASE_NAME}
	default-character-set = utf8
	ENDCNF
	echo " OK"
}

load_schema() {
	if [ ! -e schema.sql ]; then
		echo "Error: schema.sql not found."
		exit 1
	fi
	echo -n "Loading table schema…"
	mysql ${DB_OPT} < schema.sql
	echo " OK"
}

migrate() {
	echo "Running migrations…"
	python manage.py migrate
}

[ -z "$1" ] && usage

if [ -z ${DATABASE_NAME} ]; then
	echo "Error: database configuration unavailable."
	echo "Ensure .env is setup properly and this script is run from the virtualenv"
	exit 1
fi

case "$1" in
	init)
		create_user
		create_db
		gen_cnf
		migrate
		load_schema
		;;
	drop)
		drop_db
		drop_user
		;;
	reset)
		drop_db
		create_db
		migrate
		load_schema
		;;
	*)
		usage
esac

echo
echo "Done"
