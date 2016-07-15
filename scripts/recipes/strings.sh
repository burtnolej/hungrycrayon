#!/bin/bash

function spacepad {

	# passed args
	content=$1  # the string to pad
	strlen=$2 # the length of the result str (len(pad)+len(content))
	padchar=$4 # the char to pad with
	just=$3 # left / right

	# init working variables
	padstr=""
	i=0

	# work out the size of pad needed
	contentlen=${#content}
	lenpad=$[$strlen-$contentlen]

	# create a str of char=padchar x lenpad
	while [ $i -lt "$lenpad" ]
	do
        	i=$[$i+1]
        	padstr=$padstr$padchar
	done
	
	# apply justify instructions
        if [ $just = "left" ]; then
		echo $padstr$content
	else
		echo $content$padstr
	fi
}

function writelog {

	# passed args
	content=$1 # the string to pad
	strlen=$2 # the length of the result content str 
	padchar=$3 # the char to pad with
	just=$4 # left/right
	metalength=11 # the target len of non content fields (like date)

	# init
	padresult=""

	# get meta data for log
	base=`basename "$0"` # caller script name
	rundate=`date +"%m-%d-%y"` #date
	runtime=`date +"%H:%M:%S"` #time

	# create list of all metadataitems to output
	metalist=( $base $rundate $runtime )

	IFS='%'
	# iterate and pad each element with default padlen
	for meta in "${metalist[@]}"
	do
		padresult=$padresult$(spacepad $meta $metalength $just $padchar)
        	
	done

	# pad content with user def len
	padresult=$padresult$(spacepad $content $strlen $just $padchar)

	# put on stdout
	echo $padresult
	unset IFS
}

writelog "foobar" 20 "_" "left"
writelog "foobar" 40 "-" "right"
writelog "foobar" 40 " " "right"
unset IFS
