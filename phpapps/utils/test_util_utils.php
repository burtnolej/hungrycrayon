<?php

$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);
require_once 'autoload.php';
include_once 'utils_utils.php';
include_once 'test_utils.php';

class test_file extends PHPUnit_Framework_TestCase
{
	public function test_writefile()
	{
		$filename = "/tmp/phpfile.txt";
		$content = "foobar";
		$mode = "w";
		writetofile($filename,$content,$mode);
	}
	
	public function test_readfile()
	{
		$filename = "/tmp/phpfile.txt";
		$content = "foobar";
		$mode = "w";
		writetofile($filename,$content,$mode);

		$this->assertEquals(readfromfile($filename),$content);
	}
}

set_error_handler("handleError");
   
try {
	/* file */
	testrunner("file");
} catch (Exception $e) {
	echo 'Caught exception: ',  $e->getMessage(), "\n";
}

?>