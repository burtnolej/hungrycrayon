<?php

include "utils_utils.php";

class utils_test {

	// create store for results
	private static $tests = array();
	private static $results = array();
	private static $message = array();
		
	// holds the id of the current test being executed by runner
	private static $lasttestid=-1;  
		
	private function __register($test_name) {
		utils_test::$lasttestid++;
		
		utils_test::$tests[utils_test::$lasttestid] =$test_name;
		utils_test::$results[utils_test::$lasttestid] = boolstr(true);
		utils_test::$message[utils_test::$lasttestid] = '';
	}
	
	private function __setmessage($message){
		utils_test::$message[utils_test::$lasttestid] = $message;
	}
	
	private function __setresult($result){
		utils_test::$results[utils_test::$lasttestid] = $result;
	}
	
	function runner() {
		
		$class_name=get_class($this);
		
		foreach (get_class_methods(get_class($this)) as $func) {

			if (substr($func,0,5) == "test_") {
				$this->__register($func);
				call_user_func(get_class($this).'::'.$func);
			}
		}
	}
	
	function assert_true($actual_result) {
	   if ($actual_result == false) {
	   	$this->__setresult(boolstr(false));
	   	$this->__setmessage(sprintf(">>> %s != %s",boolstr($actual_result), 								boolstr(true)));
	   } 
	}
	
	function output_results() {

		for ($i=0;$i<=utils_test::$lasttestid+1;$i++) {
			echo utils_test::$tests[$i]."  ".utils_test::$results[$i]. "  ".
				utils_test::$message[$i].PHP_EOL;
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