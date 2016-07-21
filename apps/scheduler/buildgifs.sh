#!/bin/bash

days=( "Monday" "Tuesday" "Wednesday" "Thursday" "Friday" )

function generategif {

	bg=$1
	fill=$2
	psize=$3
	label=$4

	fname="$4-$3-$3-$1.gif"
	exec="convert -background $bg -fill $fill -pointsize $psize label:$label $fname"

	`$exec`
}

# times
i=9
while [ $i -lt 17 ]
do 
        label="$i:00"
	generategif white black 12 $label
        i=$[$i+1]
done

# day

for day in "${days[@]}"
do
	generategif white black 12 $day
done
