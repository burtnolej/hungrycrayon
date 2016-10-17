#!/bin/bash

sourcedir="../schoolschedulewizard"
targetdir="."

files=( "ssloader.py" "ssviewer.py" "sswizard_utils.py" "sswizard_query_utils.py" "dbtableviewer.py" )

for file in "${files[@]}"
do 
        exec_str="cp -r "$sourcedir/$file" "$targetdir/$file
	echo $exec_str
	`$exec_str`

done



