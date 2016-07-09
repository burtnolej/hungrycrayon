<?php

error_reporting(E_STRICT);

include "utils_utils.php";

class utils_test {

	// create store for results
	private static $tests = array();
	private static $current_test = null;
		
	private function __register($test_name) {
		//utils_test::$lasttestid++;
		
		$test = new StdClass();
		$test->name = $test_name;
		$test->result = boolstr(true);
		$test->message = '';
		utils_test::$tests[] = $test;
		utils_test::$current_test = $test;
	}
	
	private function __formatmessage($test) {
		$msg = sprintf("%s|%s|%s",
					str_pad($test->name,20," "),
					str_pad($test->result,5," "),
					str_pad($test->message,30," "));

		return($msg);
	}
	
	function runner() {
		
		$class_name=get_class($this);
		
		foreach (get_class_methods(get_class($this)) as $func) {

			if (substr($func,0,5) == "test_") {
				$this->__register($func);
				call_user_func(array($this,$func));
			}
		}
	}
	
	function output_results() {

		foreach (utils_test::$tests as $test) {
			echo $this->__formatmessage($test).PHP_EOL;
		}	
	}

	function assert_true($actual_result) {
		
		$test = utils_test::$current_test;
		
	   if ($actual_result == false) {
	   	$test->result = boolstr(false);
	   	$test->message = sprintf(">>> %s != %s",boolstr($actual_result), 										boolstr(true));
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
}

?>