#!/bin/bash

dbname="$1.sqlite3"
#dbname=tmp.sql
tablename=$2
#tablename=foobar
coldefn=$3
#coldefn="col1 text,col2 text,col3 text"

if [ "$dbname" = "" ] || [ "$tablename" = "" ] || [ "$coldefn" = "" ]; then 
	echo "usage: db_create.sh dbname tablename coldefn"
	echo "       dbname = 'name' (gets appended with .sqlite3)"
	echo "       coldefn = 'name1 text name2 text name3 text'"
	exit
fi

sqlite3 -batch $dbname <<EOF
.headers on
.mode column
.open $dbname
CREATE TABLE $tablename ($coldefn);
EOF
