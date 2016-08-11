#!/bin/bash

sqlite3 -batch $1 <<EOF
.headers on
.mode column
.open "tmp.sql"
CREATE TABLE foobar ('__col1' 'text');
EOF
