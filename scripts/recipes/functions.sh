#!/bin/bash

function spacepad {

	echo "arg1="$1",arg2="$2
}

function writelog {

	pad=$(spacepad 'foo' 'bar')

	echo $pad
}

writelog
