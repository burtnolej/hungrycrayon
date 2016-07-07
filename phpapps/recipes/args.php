
<?php

// as reference
function test_multiply_by_unpacked($val1,$val2) {
	$val1 = $val1 * $val2;
}

// as reference
function test_multiply_by_byref(&$val1,&$val2) {
	$val1 = $val1 * $val2;
}

// as reference
function test_multiply_by_weaktype(int &$val1,int &$val2) {
	$val1 = $val1 * $val2;
}


function my_error_handler($errno, $errstr, $errfile, $errline) {
	if ( E_RECOVERABLE_ERROR===$errno ) {
		print ("\n\ncaught a normally fatal error\n");
		print ("Error number: $errno\n");
		print ("Error string: $errstr\n");
		print ("Error file: $errfile\n");
		print ("Error line: $errline\n");
	return true;
 }
 return false;
}


// main //
$base_val=10;
$multiplier=5;
$arg_array = array("val1"=>10,"val2"=>5);

//test_multiply_by_byref($base_val,$multiplier);

// test passing in unpacked set of args
test_multiply_by_unpacked(array($base_val,$multiplier));


//echo $base_val;

//$base_val=10.4;
//$multiplier=4.7;

//set_error_handler("my_error_handler");
//try {

test_multiply_by_weaktype($base_val,$multiplier);
//} catch(Exception $e){
//	echo 'Caught exception: ',$e->getMessage(),"\n";
//}
//echo $base_val;


?>
