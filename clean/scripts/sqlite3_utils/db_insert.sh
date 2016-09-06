#!/bin/bash

data="('a','a1','a2'),('b','b1','b2')"
coldefn="col1,col2,col3"

sqlite3 -batch $1 <<EOF
.headers on
.mode column
.open "tmp.sql"
INSERT INTO foobar ($coldefn) VALUES $data;
EOF
