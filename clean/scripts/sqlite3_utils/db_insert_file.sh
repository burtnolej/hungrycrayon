#!/bin/bash

datafile=$1
#datafile="datarows.txt"
dbname=$2".sqlite3"
#dbname=tmp.sql
tablename=$3
#tablename=foobar

if [ "$datafile" = "" ] || [ "$dbname" = "" ] || [ "$tablename" = "" ]; then
        echo "usage: db_insert_file.sh filename dbname tablename"
        exit
fi

rowcount=0
while IFS='' read -r line || [[ -n "$line" ]]; do

	if [ "$rowcount" = 0 ]; then 
		colname=$line
	elif [ "$rowcount" = 1 ]; then
		coldefn=$line
	elif [ "$rowcount" = 2 ]; then
		data="($line)"
	else
		data=$data",($line)"
	fi
	rowcount=$((rowcount+1))
done < "$datafile"


sqlite3 -batch $dbname <<EOF
.headers on
.mode column
.open $dbname
CREATE TABLE $tablename ($coldefn);
EOF

sqlite3 -batch $dbname <<EOF
.headers on
.mode column
.open $dbname
INSERT INTO $tablename ($colname) VALUES $data;
EOF

./db_dump_all.sh $dbname
