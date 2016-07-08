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
	
class ErrorHelper {

	function pprint_stack($basename,$funcname,$lineno,$args,$fulltrace,$padstr=" ") {	
		
		printf("%s|%s|%s|%s|%s\n",str_pad($basename,20,$padstr),
									str_pad($funcname,30,$padstr),
									str_pad($lineno,10,$padstr),
									str_pad($args,30,$padstr),"");
									//str_pad($fulltrace,150,$padstr));
	}
	
	function exception_handler($e) {
	
	
		print_r($e);
		echo PHP_EOL.'Exception: ',$e->getMessage(),"\n\n";
		$stack_as_array = explode("\n",$e->getTraceAsString());
		$i=0;
		pprint_stack('basename','funcname','lineno','args','fulltrace');
		pprint_stack('','','','','','-');
		
		foreach ($stack_as_array as $frame) {
			
			// make sure full frame output line
			if (strpos($frame,':') !== false) {
				
					// split frame by colon into 3 vars
					list($fullpath, $rest) = explode(":",substr($frame,3));
					
					// find the start of the args in the non path section
					$open_bracket_posn = strpos($rest,'(');
						
					// put args into an array
					$args_str = substr($rest,$open_bracket_posn+1,-1);
					
					// get the func name 
					$func_name = substr($rest,1,$open_bracket_posn-1);
									
					// get the lineno
					$open_bracket_posn = strpos(basename($fullpath),'(');
					$lineno = substr(basename($fullpath),$open_bracket_posn+1,-1);
					
					// get the source file basename
					$basename = substr(basename($fullpath),0,$open_bracket_posn);
					
					pprint_stack($basename, $func_name, $lineno, $args_str,$frame);
			}
		}
		echo PHP_EOL;	
	}
		

	public static function my_error_handler($errno, $errstr, $errfile, $errline) {
	
		if (strpos($errstr,'must be of the type array') == true) {
			throw new Exception("parameter must be array");
		}
		elseif (strpos($errstr,'must be an instance of SimpleXMLElement') == true) {
			throw new Exception("parameter must be as instance of SimpleXMLElement");
		}
		else {
			//echo $errstr.PHP_EOL.PHP_EOL;
			
			$stackframes= debug_backtrace();
			
			// process first frame as we know this from the
			$fframe = array_shift($stackframes);
			
			print_r($fframe);
	
			__echoif($fframe,'line');
			__echoif($fframe,'function');
			
			echo $fframe['args'][1].PHP_EOL.PHP_EOL;
			
			//echo $fframe['function'];			
			//echo $fframe['line'];			
			echo $fframe['args'][0];			
			
			$scope="";
			foreach ($fframe['args'][4] as $varname=>$val) {
				if (is_printable($val)) {
					$scope = $scope.$varname.'=>'.$val.",";
				}
				else {
					$scope = $scope.$varname.'=>'.gettype($val).",";
				}
			}
			echo $scope.PHP_EOL;;
			
			foreach ($stackframes as $frame) {
				__echoif($frame,'line');
				__echoif($frame,'function');

				$argstr="(";
				foreach (array_values($frame['args']) as $arg) {
					if (in_array(gettype($arg),array('integer','string'))) {
						$argstr = $argstr.$arg;
					}
					else {
						$argstr = $argstr.gettype($arg);
					}
				}
				$argstr = $argstr.")";
				echo $argstr.PHP_EOL;
			}
			
			trigger_error("Fatal error", E_USER_ERROR);
		}
	}
}

function is_printable($element) {
	if (in_array(gettype($element),array('integer','string')) == true) {
		return true;
	}
	return false;
}

	
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

function test_exception_handler_fatal() {
	
	set_error_handler('\\ErrorHelper::my_error_handler');
		
	function dummy() {
		trigger_error("Fatal error", E_USER_ERROR);
	}
	
	dummy();
	//$test="get item";
	//$expected_result = true;
	
	//assert_true($expected_result,$xmlutils->is_SimpleXMLElement($item),
	//						$result_bool,$result_str);
	//output_results($result_bool,$result_str,$test);	
}


function test_exception_handler_1level_fatal() {
	
	set_error_handler('\\ErrorHelper::my_error_handler');
	
	trigger_error("Fatal error", E_USER_ERROR);
	
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
//__run_tests($args);
	
	
	
/*
	switch ($argv[1]) {
	case run_switch::alltests:
		run_tests($args);
		break; 

	case run_switch::listtests:

		run_tests($args);
		break;
		
	case run_switch::test:
		if ($argv[2] == "") {
			__usage();
		}
		
		$args['testname'] = $argv[2];
		run_tests($args);
		break; 
	default:
		__usage();
		break;
*/

?>