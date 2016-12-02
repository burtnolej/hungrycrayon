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
	
	public function test_default()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
	 	$default=3;
	 	
		ob_start(); 
		
		$this->expected_result = '<label for="foobar" >foobar</label><input type="text" name="foobar" id="foobar" list="suggestions0" value="3"><datalist id="suggestions0"><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></datalist>';
						
		$_result = gethtmldropdown($column,$values,$widgetcount,$default);
					
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
		$xml = "<root>
		          <dropdown id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></dropdown>
		          <dropdown id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </dropdown>
		        </root>";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="xaxis" >xaxis</label><input type="text" name="xaxis" id="xaxis" list="suggestions0"><datalist id="suggestions0"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div><div class="container"><label for="yaxis" >yaxis</label><input type="text" name="yaxis" id="yaxis" list="suggestions1"><datalist id="suggestions1"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div>';
										
		gethtmlxmldropdown($xml);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_default()
	{
		$xml = "<root>
		          <dropdown id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <default>dow</default>
		           </dropdown>
		            
		          <dropdown id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		            <default>subject</default>
		          </dropdown>
		        </root>";

		ob_start(); 
		
		$this->expected_result = '<div class="container"><label for="xaxis" >xaxis</label><input type="text" name="xaxis" id="xaxis" list="suggestions0" value="dow"><datalist id="suggestions0"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div><div class="container"><label for="yaxis" >yaxis</label><input type="text" name="yaxis" id="yaxis" list="suggestions1" value="subject"><datalist id="suggestions1"><option>period</option><option>dow</option><option>adult</option><option>subject</option></datalist></div>';
												
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
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"/><label for="adult" >adult</label><br></td></tr><tr><td><input id="student" type="checkbox" name="ingredients[]" value="student"/><label for="student" >student</label><br></td></tr><tr><td><input id="period" type="checkbox" name="ingredients[]" value="period"/><label for="period" >period</label><br></td></tr><tr><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label><br></td></tr><tr><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label><br></td></tr><tr><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label><br></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label><br></td></tr><tr><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label><br></td></tr><tr><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label><br></td></tr><tr><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label><br></td></tr></table>';
														
		getdbhtmlmultiselect($dbname,$query,$name);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_maxy3()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		ob_start(); 
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"/><label for="adult" >adult</label><br></td><td><input id="student" type="checkbox" name="ingredients[]" value="student"/><label for="student" >student</label><br></td><td><input id="period" type="checkbox" name="ingredients[]" value="period"/><label for="period" >period</label><br></td></tr><tr><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label><br></td><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label><br></td><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label><br></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label><br></td><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label><br></td><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label><br></td></tr><tr><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label><br></td></tr></table>';
														
		getdbhtmlmultiselect($dbname,$query,$name,2);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_default()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		$checked = array('adult','student','period');
		ob_start();
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"checked/><label for="adult" >adult</label><br></td></tr><tr><td><input id="student" type="checkbox" name="ingredients[]" value="student"checked/><label for="student" >student</label><br></td></tr><tr><td><input id="period" type="checkbox" name="ingredients[]" value="period"checked/><label for="period" >period</label><br></td></tr><tr><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label><br></td></tr><tr><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label><br></td></tr><tr><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label><br></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label><br></td></tr><tr><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label><br></td></tr><tr><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label><br></td></tr><tr><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label><br></td></tr></table>';
																
		getdbhtmlmultiselect($dbname,$query,$name,0,$checked);
				
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_default_row5()
	{
		$dbname = "test_gethtmlmultiselect.sqlite";
		$query = "select name from sqlite_master";
		$name = "ingredients";

		$checked = array('adult','student','period');
		ob_start();
		
		$this->expected_result = '<table><tr><td><input id="adult" type="checkbox" name="ingredients[]" value="adult"checked/><label for="adult" >adult</label><br></td><td><input id="student" type="checkbox" name="ingredients[]" value="student"checked/><label for="student" >student</label><br></td><td><input id="period" type="checkbox" name="ingredients[]" value="period"checked/><label for="period" >period</label><br></td><td><input id="dow" type="checkbox" name="ingredients[]" value="dow"/><label for="dow" >dow</label><br></td><td><input id="lessontype" type="checkbox" name="ingredients[]" value="lessontype"/><label for="lessontype" >lessontype</label><br></td><td><input id="subject" type="checkbox" name="ingredients[]" value="subject"/><label for="subject" >subject</label><br></td></tr><tr><td><input id="synonyms" type="checkbox" name="ingredients[]" value="synonyms"/><label for="synonyms" >synonyms</label><br></td><td><input id="recordtype" type="checkbox" name="ingredients[]" value="recordtype"/><label for="recordtype" >recordtype</label><br></td><td><input id="session" type="checkbox" name="ingredients[]" value="session"/><label for="session" >session</label><br></td><td><input id="lesson" type="checkbox" name="ingredients[]" value="lesson"/><label for="lesson" >lesson</label><br></td></tr></table>';
																		
		getdbhtmlmultiselect($dbname,$query,$name,5,$checked);
				
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<span ><select id="foobar" name="foobar"><option value="1">1</option><option value="2"selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></span>';
						
		$_result = gethtmlselect($column,$values,$widgetcount,2);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_label()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<span ><label for=number>number</label><select id="foobar" name="foobar"><option value="1">1</option><option value="2"selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></span>';
								
		$_result = gethtmlselect($column,$values,$widgetcount,2,"number");
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_class()
	{
		$column = "foobar";
		$values = array(1,2,3,4,5);
		$widgetcount = 0;
		
		ob_start(); 
		
		$this->expected_result = '<span class ="class1"><select class ="class2" id="foobar" name="foobar"><option value="1">1</option><option value="2"selected>2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option></select></span>';
										
		$_result = gethtmlselect($column,$values,$widgetcount,2,NULL,NULL,"class1","class2");
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($this->expected_result,$result);
	}
}

class test_gethtmlxmlselect extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></select>
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </select>
		        </root>";

		ob_start(); 
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		$this->expected_result = '<span ><select id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><br><br><span ><select id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><br><br>';
												
		gethtmlxmlselect($xml,$defaults);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_labels()
	{
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></select>
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </select>
		        </root>";

		ob_start(); 
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		$this->expected_result = '<span ><label for=xaxis>xaxis</label><select id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><br><br><span ><label for=yaxis>yaxis</label><select id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><br><br>';
														
		gethtmlxmlselect($xml,$defaults,TRUE);
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_class()
	{
		$xml = "<root>
		          <select id='1'>
		            <field>xaxis</field>
		            <values>
		              <value>period</value>
		          	  <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values></select>
		          <select id='2'>
		            <field>yaxis</field>
		            <values>
		              <value>period</value>
		              <value>dow</value>
		              <value>adult</value>
		              <value>subject</value>
		            </values>
		          </select>
		        </root>";

		ob_start(); 
		
		$defaults = array("xaxis" => "adult", "yaxis" => "dow");
		$this->expected_result = '<span class ="class1"><select class ="class2" id="xaxis" name="xaxis"><option value="period">period</option><option value="dow">dow</option><option value="adult"selected>adult</option><option value="subject">subject</option></select></span><br><br><span class ="class1"><select class ="class2" id="yaxis" name="yaxis"><option value="period">period</option><option value="dow"selected>dow</option><option value="adult">adult</option><option value="subject">subject</option></select></span><br><br>';
														
		gethtmlxmlselect($xml,$defaults,FALSE,FALSE,"class1","class2");
					
		$result = ob_get_contents();
		ob_end_clean();
	
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmllabel extends PHPUnit_Framework_TestCase
{
	public function test_()
	{

		$label = "foobar";
		ob_start(); 
		
		$this->expected_result = '<label for=foobar>foobar</label>';
										
		gethtmllabel($label);
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

class test_gethtmlswitch extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		ob_start(); 
		
		$this->expected_result = '<link rel="stylesheet" type="text/css" href="switch.css" /><label class="switch"><input id="foobar" type="checkbox" name="foobar"><div class="slider"></div></label>';
												
		gethtmlswitch("foobar","foobar");
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_checked()
	{
		ob_start(); 
		
		$this->expected_result = '<link rel="stylesheet" type="text/css" href="switch.css" /><label class="switch"><input id="foobar" type="checkbox" name="foobar"checked><div class="slider"></div></label>';														
		gethtmlswitch("foobar","foobar",array("foobar"));
					
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
}

$stf = new test_gethtmldropdown();
$stf->test_();
$stf->test_default();

$stf = new test_gethtmldbdropdown();
$stf->test_();

$stf = new test_gethtmlxmldropdown();
$stf->test_();
$stf->test_default();

$stf = new test_gethtmlbutton();
$stf->test_();

$stf = new test_gethtmlmultiselect();
$stf->test_();
$stf->test_default();
$stf->test_maxy3();
$stf->test_default_row5();

$test = new test_gethtmlselect();
$test->test_();
$test->test_label();
$test->test_class();

$test = new test_gethtmlxmlselect();
$test->test_();
$test->test_labels();
$test->test_class();

$test = new test_gethtmllabel();
$test->test_();

$test = new test_gethtmlswitch();
$test->test_();
$test->test_checked();


?>