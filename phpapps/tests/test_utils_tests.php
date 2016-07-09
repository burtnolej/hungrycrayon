<?php
//error_reporting(E_STRICT);
include "../utils/utils_test.php";

function __get_expected_results(array $results) {
	// simple function to help with the generation of expected results
	$_expected_results=array();
	
	foreach ($results as $name=>$result) {
		$_expected_results[$name] = get_stdobject($result);
	}

	return $_expected_results;	
}	

function __check_results($func,$tests,$expected_results) {
	$results = $tests->compare_results($expected_results);
	if ($results[0] == false) {
		echo "failed:".$func."(".$results[1].")".PHP_EOL;
	}
	else {
		echo "passed:".$func.PHP_EOL;
	}
}
// -----------------------------------------------------------
// Test assert_true; true=true and true=false
// -----------------------------------------------------------
class test_asserttrue extends utils_test {
	
	public $expected_result = 'true';
	
	function test_asserttrue_1() {
		// positive test
		$this->assert_true($this->mytruefunc());
	}	

	function test_asserttrue_2() {
		// negative test
		$this->assert_true($this->myfalsefunc());	
	}
	
	function myfalsefunc() {
		return false;
	}
	
	function mytruefunc() {
		return true;
	}
}

// Expected results
$_tmp = array('test_asserttrue_1' => array('name'=>'test_asserttrue_1',
											'result'=>'true'),
														
					'test_asserttrue_2' => array('name'=>'test_asserttrue_2',
											'result'=>'false',
											'message'=>'failed:false != true'));
$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_asserttrue;
$tests->runner();
$tests->get_results();

__check_results('test_asserttrue',$tests,$expected_results);

// -----------------------------------------------------------
// Test str_equal; 'foobar'='foobar' and 'foobar'='barfoo'
// -----------------------------------------------------------
class test_str_equal extends utils_test {
	
	public $expected_result = 'foobar';
	
	function test_str_1() {
		// positive test
		$this->assert_str_equal($this->mytruefunc());
	}	

	function test_str_2() {
		// negative test
		$this->assert_str_equal($this->myfalsefunc());	
	}
	
	function myfalsefunc() {
		return 'barfoo';
	}
	
	function mytruefunc() {
		return 'foobar';
	}
}

// Expected results
$_tmp = array('test_str_1' => array('name'=>'test_str_1',
											'result'=>'true'),
														
					'test_str_2' => array('name'=>'test_str_2',
											'result'=>'false',
											'message'=>'failed:barfoo != foobar'));
$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_str_equal;
$tests->runner();
$tests->get_results();

__check_results('test_str_equal',$tests,$expected_results);


?>