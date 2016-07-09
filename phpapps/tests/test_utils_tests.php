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
	
	function test_asserttrue_1() {
		$this->assert_true(true);
	}	

	function test_asserttrue_2() {
		$this->assert_true(false);	
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
// Test equal for str 'foobar'='foobar' and 'foobar'='barfoo'
// -----------------------------------------------------------
class test_str_equal extends utils_test {
	
	function test_str_equal_1() {
		$this->assert_equal('foobar','foobar');
	}	

	function test_str_equal_2() {
		$this->assert_equal('barfoo','foobar');	
	}
}

// Expected results
$_tmp = array('test_str_equal_1' => array('name'=>'test_str_equal_1',
											'result'=>'true'),
														
					'test_str_equal_2' => array('name'=>'test_str_equal_2',
											'result'=>'false',
											'message'=>'failed:barfoo != foobar'));
$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_str_equal;
$tests->runner();
$tests->get_results();

__check_results('test_str_equal',$tests,$expected_results);

// -----------------------------------------------------------
// Test equal for int 100=100 and 100=666
// -----------------------------------------------------------
class test_int_equal extends utils_test {
	
	function test_int_equal_1() {
		$this->assert_equal(100,100);
	}	

	function test_int_equal_2() {
		$this->assert_equal(100,666);	
	}
}

// Expected results
$_tmp = array('test_int_equal_1' => array('name'=>'test_int_equal_1',
											'result'=>'true'),
														
					'test_int_equal_2' => array('name'=>'test_int_equal_2',
											'result'=>'false',
											'message'=>'failed:100 != 666'));
$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_int_equal;
$tests->runner();
$tests->get_results();

__check_results('test_int_equal',$tests,$expected_results);


// -----------------------------------------------------------
// Test str contains x in xyz = true ; a not in xyz = false
// -----------------------------------------------------------
class test_str_contains extends utils_test {

	function test_str_contains_1() {
		$this->assert_str_contains('xyz','x');
	}	

	function test_str_contains_2() {
		$this->assert_str_contains('xyz','a');	
	}
}

// Expected results
$_tmp = array('test_str_contains_1' => array('name'=>'test_str_contains_1',
											'result'=>'true'),
														
					'test_str_contains_2' => array('name'=>'test_str_contains_2',
											'result'=>'false',
											'message'=>'failed:xyz does not contain a'));
$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_str_contains;
$tests->runner();
$tests->get_results();

__check_results('test_str_contains',$tests,$expected_results);


// -----------------------------------------------------------
// Test array_equals 
// -----------------------------------------------------------
class test_array_equal extends utils_test {
	
	public $a1 = array(1,2,3,4);
	public $a2 = array(2,3,4);
	public $a3 = array(1,2,3,5);
	
	function test_array_equal_1() {
		$this->assert_array_equal($this->a1,$this->a1);
	}	
	
	function test_array_equal_2() {
		$this->assert_array_equal($this->a1,$this->a2);
	}	

	function test_array_equal_3() {
		$this->assert_array_equal($this->a1,$this->a3);
	}

}

// Expected results
$_tmp = array('test_array_equal_1' => array('name'=>'test_array_equal_1',
											'result'=>'true'),
																							
					'test_array_equal_2' => array('name'=>'test_array_equal_2',
											'result'=>'false',
											'message'=>'failed:4 len != 3 len'),
											
					'test_array_equal_3' => array('name'=>'test_array_equal_3',
											'result'=>'false',
											'message'=>'failed:[3]=>4 != [3]=>5'));

$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_array_equal;
$tests->runner();
$tests->get_results();

__check_results('test_array_equal',$tests,$expected_results);

// -----------------------------------------------------------
// Test raises exception 
// -----------------------------------------------------------
class test_raises extends utils_test {
	
	function test_raises_1() {
		$this->assert_raises(raise_ex);
	}	

	function test_raises_2() {
		$this->assert_raises(do_nothing);
	}	
	
	function raise_ex() {
		throw new Exception();
	}
	
	function do_nothing() {
		pass;
	}

}

// Expected results
$_tmp = array('test_raises_1' => array('name'=>'test_raises_1',
											'result'=>'true'),
																							
					'test_raises_2' => array('name'=>'test_raises_2',
											'result'=>'false',
											'message'=>'failed:Exception not raised'));

$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_raises;
$tests->runner();
$tests->get_results();

__check_results('test_raises',$tests,$expected_results);

// -----------------------------------------------------------
// Test exception raised contains string 
// -----------------------------------------------------------
class test_raise_contains extends utils_test {
	
	function test_raise_contains_1() {
		$this->assert_raises(raise_ex,'Exception','foobar');
	}	

	function test_raise_contains_2() {
		$this->assert_raises(raise_ex,'Exception','blahblah');
	}	
	
	function raise_ex() {
		throw new Exception('foobar');
	}
}

// Expected results
$_tmp = array('test_raise_contains_1' => array('name'=>'test_raise_contains_1',
											'result'=>'true'),
																							
					'test_raise_contains_2' => array('name'=>'test_raise_contains_2',
											'result'=>'false',
											'message'=>'failed:ex_msg foobar does not contain blahblah'));

$expected_results = __get_expected_results($_tmp);

// Run test
$tests = new test_raise_contains;
$tests->runner();
$tests->get_results();

__check_results('test_raise_contains',$tests,$expected_results);

?>