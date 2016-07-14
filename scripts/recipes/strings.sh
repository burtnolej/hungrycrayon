#!/bin/bash

function spacepad {
        fullpad=$(printf '%0.1s' "-"{1..60})
        strlen=${#1}
        padlen=${#fullpad}-$2+$strlen
        pad=${fullpad:$padlen}
        padresult=$padresult$pad$1
}

function writelog {

	base=`basename "$0"`
	spacepad $base $2
	
	rundate=`date +"%m-%d-%y"`
	spacepad $rundate $2

	runtime=`date +"%H:%M:%S"`
	spacepad $runtime $2

	spacepad $1 $2

	echo $padresult
}

writelog "foobar" 11
