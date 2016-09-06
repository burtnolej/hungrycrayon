#!/bin/bash

tbl_name=$2

sqlite3 -batch $1 <<EOF
.headers on
.mode column

select count(*) from ${tbl_name};

EOF
