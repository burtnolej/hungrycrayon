<?php

function _exec($cls,$func) {
	echo "   ->".$func." : ";
	$cls->$func();
	echo ":ok".PHP_EOL;
}
	
function testrunner($name,$func=NULL) {
	
	$testname = "test_".$name;
	echo PHP_EOL.PHP_EOL.$testname.PHP_EOL;
	$cls = new $testname();
	
	if ($func <> NULL) {
		_exec($cls,$func);
		return;
	}
	
	foreach (get_class_methods($cls) as $func) {
		
		if (substr($func,0,5) == "test_") {
			_exec($cls,$func);
		}
	}
	return($cls);
}
   
   function handleError($errno, $errstr,$error_file,$error_line) {
   		echo PHP_EOL.PHP_EOL;
      echo "Error:[$errno] $errstr - $error_file:$error_line";
      echo PHP_EOL;
      
      die();
   }
   
 ?>