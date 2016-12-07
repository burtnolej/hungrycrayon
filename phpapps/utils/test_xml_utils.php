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
		
		function xml_iter($root){
			foreach ($root as $tag => $node) {
				echo trim($tag);
				echo trim($node);
				foreach ($node->attributes() as $attr=>$value) {
						echo $attr.$value;
				}
				if (sizeof($node ->children()) <> 0) {
					 xml_iter($node);
				}
			}
		}

		$myecho = function ($str1,$str2) {
			echo trim($str1);
			echo trim($str2);
				foreach ($str2->attributes() as $attr=>$value) {
						echo $attr.$value;
				}
		};
		//xml_iter($utilsxml);
		
		$utilsxml->xml_iter($myecho);
		
		$result = ob_get_contents();
		ob_end_clean();	
		
		$this->assertEquals($result,$this->expected_results);
	}
}

//$test = new test_get_item();
//$test->test_();

//$stf = new test_xml_add_node();
//$stf->test_add_end();

$test = new  test_xml_iter();
$test->test_();

?>