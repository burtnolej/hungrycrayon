<?php

//error_reporting(E_STRICT);

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
		$test->message = 'passed';
		utils_test::$tests[$test_name] = $test;
		utils_test::$current_test = $test;
	}
	
	private function __formatmessage($test) {
		$msg = sprintf("%s|%s|%s",
					str_pad($test->name,20," "),
					str_pad($test->result,5," "),
					str_pad($test->message,30," "));

		return($msg);
	}
	
	function compare_results(array $expected_results,$verbose=false) {
		// used when testing utils_test
		// pass in an array of StdClass with name,result,message set
		// array is indexed by testname
		// compares all properties that exist on the expected_results passed in
		foreach ($expected_results as $exp_name => $exp_test) {
			
			$test = utils_test::$tests[$exp_name];
			
			foreach (get_object_vars($exp_test) as $varname => $exp_val) {	
				if ($exp_val != $test->{$varname}) {
						$msg = sprintf("var:%s %s != %s",$varname,$exp_val, $test->{$varname});
						return array(false,$msg);
				}
				elseif ($verbose == true) {
					printf("func:%s var:%s %s == %s\n",$exp_name,$varname,$exp_val, $test->{$varname});
				}
			}
		}
		return array(true);
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
	
	function print_results() {
		// print test results to screen
		$this->get_results();
		foreach (utils_test::$tests as $test) {
			echo $test->formatmessage.PHP_EOL;
		}
	}
		
	function get_results() {
		// creates the formatted output message. separated from the print screen
		// so can be supressed at runtime. one use being to make testing the test harness easier
		foreach (utils_test::$tests as $test) {
			$test->formatmessage = $this->__formatmessage($test);
		}	
	}

	function assert_true($actual_result) {
		$test = utils_test::$current_test;
	   //if ($actual_result == false) {

	   if ($actual_result != $this->expected_result) {
	   	$test->result = boolstr(false);
	   	$test->message = sprintf("failed:%s != %s",boolstr($actual_result), 														$this->expected_result);
	   } 
	}
		
	function assert_str_equal($actual_result) {
		$test = utils_test::$current_test;
		
	   if ($actual_result != $this->expected_result) {
	   	$test->result = boolstr(false);
			$test->message = sprintf("failed:%s != %s",$actual_result,
													$this->expected_result);
	    }
	}
	
	function assert_str_contains($actual_result) {
		$test = utils_test::$current_test;
		
		$result_bool=true;
		$result_str="";
						
	   if (is_int(strpos($str,$contains)) == false) {
	   	$result_bool = false;
			$result_str = sprintf(">>> [%s]  not contain [%s]",$str,$contains).PHP_EOL;
	    }
	}
	
	
	function assert_ints_equal($actual_result) {
		$test = utils_test::$current_test;
		
		$result_bool=true;
		$result_str="";
					
	   if ($int1 != $int2) {
	   	$result_bool = false;
			$result_str = sprintf(">>> %d != %d",$int1,$int2).PHP_EOL;
	    }
	}
	
	function assert_arrays_equal($actual_result) {
		$test = utils_test::$current_test;
		
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