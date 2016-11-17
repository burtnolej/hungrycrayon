<?php

$PHPLIBPATH = getenv("PHPLIBPATH");
	
if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);
require_once 'autoload.php';

include_once 'ui_utils.php';
include_once 'utils_error.php';
include_once 'utils_utils.php';

set_error_handler('\\UtilsError::error_handler');

class test_gethtmldropdown extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<label for="foobar" >foobar</label><input type="text" name="foobar" id="foobar" list="suggestions0"><datalist id="suggestions0"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></datalist>';
				
		$_result = gethtmldropdown($column,$values,$widgetcount);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
}


class test_gethtmldbdropdown extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$dbname = "test_gethtmldbdropdown.sqlite";
		$tablename = "lesson";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="subject" >subject</label><input type="text" name="subject" id="subject" list="suggestions0"><datalist id="suggestions0"><option>Math</option><option>ELA</option><option>Engineering</option></datalist></div>';
						
		gethtmldbdropdown($dbname,$tablename);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}



class test_gethtmlbutton extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$type = "submit";
		$label = "go";

		ob_start(); 
		
		$this->expected_result = '<input type="submit" name="submit" value="go" />';
								
		gethtmlbutton($type,$label);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}



class test_gethtmlxmldropdown extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$xml = "<root><dropdown id='1'><field>xaxis</field><values><value>period</value><value>dow</value><value>adult</value><value>subject</value></values></dropdown><dropdown id='2'><field>yaxis</field><values><value>period</value><value>dow</value><value>adult</value><value>subject</value></values></dropdown></root>";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="xaxis" >xaxis</label><input type="text" name="xaxis" id="xaxis" list="suggestions0"><datalist id="suggestions0"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div><div class="container"><label for="yaxis" >yaxis</label><input type="text" name="yaxis" id="yaxis" list="suggestions1"><datalist id="suggestions1"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div>';
										
		gethtmlxmldropdown($xml);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
}



class test_gethtmlmultiselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		ob_start(); 
		
		$this->expected_result = '<input id="adult" type="checkbox" name="ingredients[]" value="adult"/><label for="adult" >adult</label><br><input id="student" type="checkbox" name="ingredients[]" value="student"/><label for="student" >student</label><br><input id="period" type="checkbox" name="ingredients[]" value="period"/><label for="period" >period</label><br><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label><br><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label><br><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label><br><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label><br><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label><br><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label><br><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label><br>';
												
		gethtmlmultiselect($dbname,$query,$name);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
}

$stf = new test_gethtmldropdown();
$stf->test_();



$stf = new test_gethtmldbdropdown();
$stf->test_();



$stf = new test_gethtmlxmldropdown();
$stf->test_();


$stf = new test_gethtmlbutton();
$stf->test_();

$stf = new test_gethtmlmultiselect();
$stf->test_();
?>