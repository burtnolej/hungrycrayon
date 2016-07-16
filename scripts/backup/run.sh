#!/bin/bash

sources=( "/bin" "/etc" "/home" "/lib" "/lib64" "/opt" "/root" "/run" "/usr" "/var" )

for source in "${sources[@]}"
do
        exec="./backup.sh --mode prod --source $source"
	`$exec`

done
