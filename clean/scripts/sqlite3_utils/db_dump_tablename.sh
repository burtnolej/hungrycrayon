#!/bin/bash

sqlite3 -batch $1 <<EOF
select name from sqlite_master;
EOF
