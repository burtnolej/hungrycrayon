#!/bin/bash

tbl_name=$2

sqlite3 -batch $1 <<EOF
.headers on
.mode column

select * from ${tbl_name};

PRAGMA table_info(${tbl_name});

EOF
