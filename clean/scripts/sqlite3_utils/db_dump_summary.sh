#!/bin/bash

./db_dump_tablename.sh $1 | ./table_dump_multi_summary.sh $1
