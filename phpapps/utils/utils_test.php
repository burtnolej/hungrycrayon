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
						$msg = sprintf("func:%s var:%s %s != %s",$exp_name,$varname,$exp_val, 
																	$test->{$varname});
						return array(false,$msg);
				}
				elseif ($verbose == true) {
					printf("func:%s var:%s %s == %s\n",$exp_name,$varname,$exp_val, 
																	$test->{$varname});
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

	   if ($actual_result != true) {
	   	$test->result = boolstr(false);
	   	$test->message = sprintf("failed:%s != %s",boolstr($actual_result), boolstr(true));
	   } 
	}
		
	function assert_equal($actual_result,$expected_result) {
		$test = utils_test::$current_test;
		
	   if ($actual_result != $expected_result) {
	   	$test->result = boolstr(false);
			$test->message = sprintf("failed:%s != %s",$actual_result,$expected_result);
	    }
	}
	
	function assert_str_contains($str,$contains) {
		$test = utils_test::$current_test;
		
		if (is_int(strpos($str,$contains)) == false) {
		   	$test->result = boolstr(false);
				$test->message = sprintf("failed:%s does not contain %s",$str,$contains);
	   }
	}
	
	function assert_array_equal($array1,$array2) {
		$test = utils_test::$current_test;
					
		$sa1 = sizeof($array1);
		$sa2 = sizeof($array2);
		
		if ($sa1 != $sa2) {
			$test->result = boolstr(false);
			$test->message = sprintf("failed:%d len != %d len",$sa1,$sa2);
		}
		else {
			foreach ($array1 as $key => $val) {
				
				if (gettype($array1[$key]) == 'array') {
					// assume this an array of array comparison
					if (!gettype($array2[$key]) == 'array') {
						$test->result = boolstr(false);
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
			   	$test->result = boolstr(false);
					$test->message = sprintf("failed:[%s]=>%s != [%s]=>%s",
												strval($key), $item1,strval($key), $item2);
			   }
			}
		}
	}
	
	function assert_raises($func,$exception_cls_name) {
		$test = utils_test::$current_test;
		$test->result = boolstr(false);
	
		try  {
				call_user_func(array($this,$func));
		}
		catch (Exception $e) {
			if (get_class($e) == $exception_cls_name) {
				$test->result = boolstr(true);
			}
		}	
	}
	
	function __run_tests(array $args) {
			
		foreach (get_defined_functions()['user'] as $func) {
			if (strpos($func,'test_') !== false) {
				call_user_func($func);
			}
		}
	}
}

?>