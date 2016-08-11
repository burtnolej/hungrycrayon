#!/bin/bash

sqlite3 -batch $1 <<EOF
.headers on
.mode column

select * from sqlite_master;
EOF
