#!/bin/bash

function spacepad {

	# passed args
	element=$1
	length=$2
	padchar=$4
	just=$3

while [ $i -lt "$lenpad" ]
do
        i=$[$i+1]
        padstr=$padchar$padstr
done

	fullpad=$(printf '%0.1s' "$padchar"{1..60})

	if [ $padchar = 'x' ]; then
		echo 

	# create a log string of pad elements
        padlen=${#fullpad}-$length+${#element}
        pad=${fullpad:$padlen}

	# return padded string back to caller
        if [ $just = "left" ]; then
		echo $pad$1
	else
		echo $1$pad
	fi
}

function writelog {

	# passed args
	content=$1
	length=$2
	padchar=$3
	just=$4
	metalength=11

	# init
	padresult=""

	# get meta data for log
	base=`basename "$0"` # caller script name
	rundate=`date +"%m-%d-%y"` #date
	runtime=`date +"%H:%M:%S"` #time

	# create list of all metadataitems to output
	metalist=( $base $rundate $runtime )

	# iterate and pad each element with default padlen
	for meta in "${metalist[@]}"
	do
		padresult=$padresult$(spacepad $meta $metalength $just $padchar)
        	
	done

	# pad content with user def len
	padresult=$padresult$(spacepad $content $length $just $padchar)

	# put on stdout
	echo $padresult
}

writelog "foobar" 20 "_" "left"
writelog "foobar" 40 "-" "right"
writelog "foobar" 40 " " "right"
