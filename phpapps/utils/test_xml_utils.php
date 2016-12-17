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

class test_get_item extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$xml = "<root>
						 	<item id='1'>
						 		<value>foobar</value>
						 	</item>
						 </root>";
					 
		$this->expected_result = 'foobar';
		
		$utilsxml = simplexml_load_string($xml,'utils_xml');
		$item =  $utilsxml->get_item(1,"item","@id");	
		
		$this->assertEquals($item->value,$this->expected_result);
	}
}

class test_xml_add_node extends PHPUnit_Framework_TestCase
{
	public function test_add_end()
	{
		$xml = "<root><item id='1'><value>foobar</value></item></root>";
		$this->expected_result  = '<root><item id="1"><value>foobar</value><foo>bar</foo></item></root>';
		
		$utilsxml = simplexml_load_string($xml,'utils_xml');
		$item =  $utilsxml->get_item(1,"item","@id");	
		$item->addchild('foo','bar');
				
		$this->assertTrue(is_int(strpos($this->expected_result,$item->asXML())));
	}
}

class test_xml_append_tree extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		
		$_xml = "<root><item id='1'><value>foobar</value></item></root>";
		$_xmlinsert = "<root><item id = '2'><value>barfoo</value></item></root>";
		
		$this->expected_result  = '<?xml version="1.0"?><root><item id="1"><value>foobar</value><item id="2"><value>barfoo</value></item></item></root>';
		
		$xml = simplexml_load_string($_xml,'utils_xml');
		$xmlinsert = simplexml_load_string($_xmlinsert,'utils_xml');
		
		$item =  $xml->get_item(1,"item","@id");	
		append_xml($xmlinsert,$item);

		$this->assertEquals(preg_replace("[\n]","",$this->expected_result),preg_replace("[\n]","",$xml->asXML()));
	}
}
	
class test_assocarray_to_xml extends PHPUnit_Framework_TestCase
{
	public function test_simple()
	{
		
		$a = array("link"=>"foobar.php");
		$expected_result = '<?xml version="1.0"?>'.PHP_EOL.'<root><link><value>foobar.php</value></link></root>';
					
		$root=new SimpleXMLElement("<root></root>");
			
		assoc_array2xml($a,$root);	
		
		echo $root->asXML();
		echo $expected_result;
		$this->assertEquals($expected_result,$root->asXML());
	}
	
	public function test_()
	{
				
		$a = array("link"=>"foobar.php", "flags" => array("flag1"=>"flagval1", "flag2" => array("flag21"=>"flag21val1")));
		$expected_result = '<?xml version="1.0"?>'.PHP_EOL.'<root><link>foobar.php</link><flags><flag1>flagval1</flag1><flag2><flag21>flag21val1</flag21></flag2></flags></root>';
							
		$root=new SimpleXMLElement("<root></root>");
			
		assoc_array2xml($a,$root);	
		
		$this->assertEquals(preg_replace("[\n]","",$expected_result),preg_replace("[\n]","",$root->asXML()));
	}
	
	public function test_customroot()
	{			
	
		$expected_result = '<?xml version="1.0"?><root><item name="foobar"><link><link>foobar.php</link><flags><flag1>flagval1</flag1><flag2><flag21>flag21val1</flag21></flag2></flags></link></item></root>';

		$a = array("link"=>"foobar.php", "flags" => array("flag1"=>"flagval1", "flag2" => array("flag21"=>"flag21val1")));					
		$root=new SimpleXMLElement("<root></root>");
		$child = $root->addChild("item");
		$child->addAttribute("name",'foobar');
		$link = $child->addChild("link");
		assoc_array2xml($a,$link);
		
		$this->assertEquals(preg_replace("[\n]","",$expected_result),preg_replace("[\n]","",$root->asXML()));
	}
}

class test_xml_iter extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		$xml = "<root>
						 	<item id='1'>
						 		<value>foobar</value>
						 	</item>
						 	<item id='2'>
						 		<item id='2.1'>
						 			<value>barfoo</value>
						 		</item>
						 	</item>
						 </root>";	
						 
	   $this->expected_results = 'itemid1valuefoobaritemid2itemid2.1valuebarfoo';
	   
		$utilsxml = simplexml_load_string($xml,'utils_xml');		

		ob_start(); 

		$myecho = function ($str1,$str2) {
			echo trim($str1);
			echo trim($str2);
				foreach ($str2->attributes() as $attr=>$value) {
						echo $attr.$value;
				}
		};
		
		$utilsxml->xml_iter($myecho);
		
		$result = ob_get_contents();
		ob_end_clean();	
		
		$this->assertEquals($result,$this->expected_results);
	}
}

$test = new test_get_item();
$test->test_();

$stf = new test_xml_add_node();
$stf->test_add_end();

$test = new  test_xml_iter();
$test->test_();

$test = new test_assocarray_to_xml();
$test->test_();
$test->test_customroot();

$test = new test_xml_append_tree();
$test->test_();

?>