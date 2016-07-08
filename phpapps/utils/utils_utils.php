<?php

abstract class run_switch
{
    const alltests = "--all-tests";
    const testname = "--test-name";
    const listtests = "--list-tests";
    const usage = "--usage";
}

function __echoif($array,$key){
	if (array_key_exists($key,$array)) {
		echo $array[$key];
	}
}
	
function is_printable($element) {
	if (in_array(gettype($element),array('integer','string')) == true) {
		return true;
	}
	return false;
}
