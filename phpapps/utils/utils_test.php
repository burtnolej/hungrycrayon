<?php

function assert_true($bool1, $bool2,
									&$result_bool,&$result_str) {
	
	$result_bool=true;
	$result_str="";
				
   if ($bool1 != $bool2) {
   	$result_bool = false;
		$result_str = sprintf(">>> %b != %b",$bool1,$bool2).PHP_EOL;
    }
}

function assert_strs_equal($str1, $str2,
									&$result_bool,&$result_str) {
	
	$result_bool=true;
	$result_str="";
				
   if ($str1 != $str2) {
   	$result_bool = false;
		$result_str = sprintf(">>> %s != %s",$str1,$str2).PHP_EOL;
    }
}

function assert_str_contains($contains, $str,
									&$result_bool,&$result_str) {
	
	$result_bool=true;
	$result_str="";
					
   if (is_int(strpos($str,$contains)) == false) {
   	$result_bool = false;
		$result_str = sprintf(">>> [%s]  not contain [%s]",$str,$contains).PHP_EOL;
    }
}


function assert_ints_equal($int1, $int2,
									&$result_bool,&$result_str) {
	
	$result_bool=true;
	$result_str="";
				
   if ($int1 != $int2) {
   	$result_bool = false;
		$result_str = sprintf(">>> %d != %d",$int1,$int2).PHP_EOL;
    }
}

function assert_arrays_equal($array1, $array2,
									&$result_bool,&$result_str) {
	
	$result_bool=true;
	$result_str="";
		
	$sa1 = sizeof($array1);
	$sa2 = sizeof($array2);
	
	if ($sa1 != $sa2) {
		$result_bool = false;
		$result_str = sprintf("array1 len=%d != array2: len=%d",
								$sa1,$sa2);
	}
	else {
		foreach ($array1 as $key => $val) {
			
			if (gettype($array1[$key]) == 'array') {
				// assume this an array of array comparison
				if (!gettype($array2[$key]) == 'array') {
					throw new Exception('both objects need to be array of arrays');
				}
				$item1 = join(",",$array1[$key]);
				$item2 = join(",",$array2[$key]);
			}
			else {
				$item1 = $array1[$key];
				$item2 = $array2[$key];
			}
			
		   if ($item1 != $item2) {
		   	$result_bool = false;
				$_result_str = sprintf(">>> array1[%d]=>%s != array2[%d]=>%s",
											$key, $item1,$key, $item2);
											
		    	$result_str = $result_str.$_result_str.PHP_EOL;
		    }
		}
	}
	
	if (!$result_bool==true) {
		$result_str = $result_str.">>> [".join($array1,",")."]".PHP_EOL;
		$result_str = $result_str.">>> [".join($array2,",")."]".PHP_EOL;
		
	}
}

function output_results($result_bool,$result_str,$test_name) {
	if ($result_bool) {
	echo "PASSED:".$test_name.PHP_EOL;
	}
	else {
		echo "FAILED:".$test_name.PHP_EOL.$result_str.PHP_EOL;
	}
}

function test_error_handler() {
	
	//set_error_handler('\\ErrorHelper::my_error_handler');
		
	function dummy() {
		throw new Exception("foobar foobar foobar");
	}
	
	dummy();
	//$test="get item";
	//$expected_result = true;
	
	//assert_true($expected_result,$xmlutils->is_SimpleXMLElement($item),
	//						$result_bool,$result_str);
	//output_results($result_bool,$result_str,$test);	
}

function __run_tests(array $args) {
	
	
	if (array_key_exists('testname',$args)) {
		call_user_func($args['testname']);
		return;
	}
	
	if (array_key_exists('alltests',$args)) {
		foreach (get_defined_functions()['user'] as $func) {
			if (strpos($func,'test_') !== false) {
				call_user_func($func);
			}
		}
	}
	
	if (array_key_exists('alltests',$args)) {
		foreach (get_defined_functions()['user'] as $func) {
			if (strpos($func,'test_') !== false) {
				call_user_func($func);
			}
		}
	}
}

?>