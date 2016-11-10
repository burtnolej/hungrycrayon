<?php

require_once __DIR__ . '/composer/vendor/autoload.php';

set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');

include_once 'db_utils.php';
include_once 'utils_error.php';
include_once 'utils_utils.php';

set_error_handler('\\UtilsError::error_handler');

class test_gettablecolumns extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$dbname = "test_gettablecolumns.sqlite";
		$tablename = "lesson";
		$result = gettablecolumns($dbname,$tablename);		
		$this->expected_result = Array('status','substatus','recordtype','enum','period','saveversion','prep','source','teacher','session','student','dow','userobjid','subject');
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_getcolumndistinctvalues extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$dbname = "test_getcolumndistinctvalues.sqlite";
		$tablename = "lesson";
		$colname = "subject";
		
		$result = getcolumndistinctvalues($dbname,$tablename,$colname);		
		$this->expected_result = Array('Engineering','Movement','Math');
		$this->assertEquals($result,$this->expected_result);
	}
}

$test_gettablecolumns = new test_gettablecolumns();
$test_gettablecolumns->test_();

$test_getcolumndistinctvalues = new test_getcolumndistinctvalues();
$test_getcolumndistinctvalues->test_();

?>
