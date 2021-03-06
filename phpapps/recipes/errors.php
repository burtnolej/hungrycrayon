<?php

// as reference; weak typing
function test_multiply_by(&$val1,&$val2) {
	
	
	
	if (!is_int($val1) or !is_int($val1)) {
		throw new Exception("args must be of type int\n");
	}
	if ($val2 < 0 or $val1 < 0) {
		throw new Exception("args must be >= 0");
	}
	$val1 = $val1 * $val2;
}

function test_multiply_by_weaktype(int $val1,$val2) {
}

function my_exception_handler($errno, $errstr, $errfile, $errline) {
	if ( E_RECOVERABLE_ERROR===$errno ) {
		print ("exception #: $errno line: $errline \n");
		//print ("Error string: $errstr\n");
		//print ("Error file: $errfile\n");
		
		//print getTraceAsString();

	return true;
 }
 return false;
}

function my_error_handler($errno, $errstr, $errfile, $errline) {
	print("error #:$errno line:$errline\n");
}


set_exception_handler("my_exception_handler");
set_error_handler("my_error_handler");


// no errors
$base_val=10;
$multiplier=5;
test_multiply_by($base_val,$multiplier);

// catch thrown exception not int
$base_val=10.3;
$multiplier=4.8;
try {
	test_multiply_by($base_val,$multiplier);
}
catch(Exception $e) {
	printf("Exception: %s", $e->getMessage());
}

// catch fatal type mismatch
$base_val=10.3;
$multiplier=4.8;
test_multiply_by_weaktype($base_val,$multiplier);

?>


try {
	test_get_sibling_details($xmlutils);
	test_get_children_details($xmlutils);
	test_get_ancestor_details($xmlutils);
	test_item_details($xmlutils);
	test_parent($xmlutils);
	test_search($xmlutils);
	test_search_int_as_string($xmlutils);
	test_search_string($xmlutils);
	test_search_top_item($xmlutils);
	test_item_depth($xmlutils);
} catch (Exception $e) {
	echo 'Caught: ',$e->getMessage(),"\n";
	echo $e->getTraceAsString(),"\n";
	
	
	function my_error_handler($errno, $errstr, $errfile, $errline) {
		
	if (strpos($errstr,'must be of the type array, string given') == false) {
		throw new Exception("1st parameter must be integer");
	}
	else {
		trigger_error("Fatal error", E_USER_ERROR);
	}
}

set_error_handler("my_error_handler");


set_error_handler('\\XMLUtils::my_error_handler');

test_get_sibling_details_arg1_int($xmlutils);
test_get_sibling_details_arg2_int($xmlutils);
test_get_sibling_details($xmlutils);
test_get_children_details($xmlutils);
test_get_ancestor_details($xmlutils);
test_item_details($xmlutils);
test_parent($xmlutils);
test_parent_bad_arg($xmlutils);
test_search($xmlutils);
test_search_int_as_string($xmlutils);
test_search_string($xmlutils);
test_search_top_item($xmlutils);
test_item_depth($xmlutils);
	