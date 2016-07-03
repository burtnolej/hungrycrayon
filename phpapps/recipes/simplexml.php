<?php

$xmlstr = <<<XML
<menu>
	<menuitemid>1</menuitemid>
	<label>root</label>
	<menuitem>
		<menuitemid>2</menuitemid>
		<label>theuppermiddle</label>
		<tag>foo</tag>
		<menuitem>
			<menuitemid>3</menuitemid>
			<label>thelowermiddle</label>
			<tag>bar</tag>
			<menuitem>
				<menuitemid>31</menuitemid>
				<label>thebottom</label>
				<tag>foobar</tag>
			</menuitem>
		</menuitem>
		<menuitem>
			<menuitemid>4</menuitemid>
			<label>thelowermiddle-sibling1</label>
			<menuitem>
				<menuitemid>41</menuitemid>
				<label>thelowermiddle-cousin1</label>
			</menuitem>
		</menuitem>
		<menuitem>
			<menuitemid>5</menuitemid>
			<label>thelowermiddle-sibling2</label>
			<menuitem>
				<menuitemid>51</menuitemid>
				<label>thelowermiddle-sibling-child1</label>
				<menuitem>
					<menuitemid>511</menuitemid>
					<label>thelowermiddle-sibling-grandchild1</label>
					<menuitem>
						<menuitemid>5111</menuitemid>
						<label>thelowermiddle-sibling-greatgrandchild1</label>
					</menuitem>
				</menuitem>
				<menuitem>
					<menuitemid>512</menuitemid>
					<label>thelowermiddle-sibling-grandchild2</label>
				</menuitem>
				<menuitem>
					<menuitemid>513</menuitemid>
					<label>thelowermiddle-sibling-grandchild3</label>
				</menuitem>
			</menuitem>
		</menuitem>
		<menuitem>
			<menuitemid>6</menuitemid>
			<label>thelowermiddle-sibling3</label>
		</menuitem>
		<menuitem>
			<menuitemid>foobar</menuitemid>
			<label>foobar-sibling</label>
		</menuitem>
	</menuitem>
</menu>
XML;

$xmlstr_alternate = <<<XML
<menu>
	<menuitem>
		<menuitemid>1</menuitemid>
		<name>jack</name>
		<menuitem>
			<menuitemid>1.1</menuitemid>
			<name>ben</name>
			<menuitem>	
				<menuitemid>1.1.1</menuitemid>
				<name>jane</name>
			</menuitem>
			<menuitem>
				<menuitemid>1.1.2</menuitemid>
				<name>jim</name>
			</menuitem>
			<menuitem>
				<menuitemid>1.1.3</menuitemid>
				<name>jamie</name>
			</menuitem>
		</menuitem>
	</menuitem>
	<menuitem>
		<menuitemid>2</menuitemid>
		<name>justin</name>
		<menuitem>
			<id>2.1</id>
			<name>joan</name>
		</menuitem>
	</menuitem>
</menu>
XML;
				

//include 'samplexml.php';
include 'xml_utils.php';
//include 'php_utils.php';

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

/*
$array1 = array('a','b','c');
$array2 = array('a','b','c','d');
$array3 = array('a','b','e');
$array4 = array('a'=>1,'b'=>2,'e'=>3);
$array5 = array('a'=>1,'b'=>4,'e'=>3);


$result_bool=true;
$result_str="";

// Test 1
assert_arrays_equal($array1,$array1,$result_bool,$result_str);
output_results($result_bool,$result_str);

// Test 2
assert_arrays_equal($array1,$array2,$result_bool,$result_str);
output_results($result_bool,$result_str);

// Test 3
assert_arrays_equal($array1,$array3,$result_bool,$result_str);
output_results($result_bool,$result_str);

// Test 4
assert_arrays_equal($array4,$array5,$result_bool,$result_str);
output_results($result_bool,$result_str);

*/

// ------------------------------------------------------------------
// search tests -----------------------------------------------------
// ------------------------------------------------------------------

function test_search($xmlutils) {
	$expected_label = 'thelowermiddle-sibling1';
	$test="search tree for specific item - new style";
	
	$item = $xmlutils->get_item(4);
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_search_int_as_string($xmlutils) {
	$test="search tree for specific item - int as a string";
	$expected_label = 'thelowermiddle-sibling1';
	
	$item = $xmlutils->get_item('4');
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_search_string($xmlutils) {
	$test="search tree for specific item - string";
	$expected_label = 'foobar-sibling';
	
	$item = $xmlutils->get_item('foobar');
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_search_top_item($xmlutils) {
	$test="search tree for top item";
	$expected_label = 'theuppermiddle';
	
	$item = $xmlutils->get_item(2);
	
	assert_strs_equal($item->label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

// ------------------------------------------------------------------
// parent tests -----------------------------------------------------
// ------------------------------------------------------------------

function test_parent($xmlutils) {
	$test="get label of parent node";
	$expected_label = 'thelowermiddle';
	
	$item = $xmlutils->get_item(31);
	$parent_label = $xmlutils->get_parent($item)->label;
	
	assert_strs_equal($parent_label,$expected_label,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_parent_bad_arg($xmlutils) {
	$test="get label of parent node - bad arg";
	$expected_results = "parameter must be as instance of SimpleXMLElement";
		
	try {
		$parent_label = $xmlutils->get_parent(31)->label;
	} catch (Exception $e) {
		assert_str_contains($expected_results,$e->getMessage(),
										$result_bool,$result_str);
	}
	
	output_results($result_bool,$result_str,$test);
}

// ------------------------------------------------------------------
// item details tests -----------------------------------------------
// ------------------------------------------------------------------

function test_item_details($xmlutils) {
	$test="get all details of node";
	$expected_results = array('tag' => 'foobar','label'=>'thelowermiddle');
	
	$item = $xmlutils->get_item(31);
	$details = $xmlutils->get_item_details($item,array('tag'),array('label'));
	
	assert_arrays_equal($details,$expected_results,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);	
}

// ------------------------------------------------------------------
// item depth tests -------------------------------------------------
// ------------------------------------------------------------------

function test_item_depth($xmlutils) {
	
	$test="get depth of node";
	$result = "PASSED:".$test;
	$expected_results = 3;

	$depth = $xmlutils->get_item_depth(41);
	
	assert_ints_equal($depth,$expected_results,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_item_depth_root($xmlutils) {
	
	$test="get depth of node";
	$result = "PASSED:".$test;
	$expected_results = 0;

	$depth = $xmlutils->get_item_depth(1);
	
	assert_ints_equal($depth,$expected_results,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}


// ------------------------------------------------------------------
// ancestor tests ---------------------------------------------------
// ------------------------------------------------------------------

function test_get_ancestor_details($xmlutils) {
	$test="get all ancestors of node from menuid";
	$result = "PASSED:".$test;
	$expected_results = array(array('menuitemid'=>4,'label'=>'theuppermiddle'),
									  array('menuitemid'=>2,'label'=>'root'),
									  array('menuitemid'=>1,'label'=>''));

	//$ancestors=$xmlutils->get_ancestors(41);
	
	$ancestor_details = $xmlutils->get_ancestor_details(41, 
															array('menuitemid'),
															array('label'));
	
	assert_arrays_equal($ancestor_details,$expected_results,
								$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);;
}

// ------------------------------------------------------------------
// siblings tests ---------------------------------------------------
// ------------------------------------------------------------------

function test_get_sibling_details($xmlutils) {

	$test="get siblings of node - overide xnode";
	$expected_results = array(array('menuitemid'=>3,'label'=>'theuppermiddle'),
									  array('menuitemid'=>4,'label'=>'theuppermiddle'),
									  array('menuitemid'=>5,'label'=>'theuppermiddle'),
									  array('menuitemid'=>6,'label'=>'theuppermiddle'),
									  array('menuitemid'=>'foobar','label'=>'theuppermiddle'));

	$sibling_details = $xmlutils->get_sibling_details(3, 
															array('menuitemid'),
															array('label'));
	
	assert_arrays_equal($sibling_details,$expected_results,
								$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);
}

function test_get_sibling_details_arg1_int($xmlutils) {

	$test="get siblings details - bad 1st arg";
	$expected_results = "1st parameter must be integer";
	
	$result_bool = false;
	
	try {
		$sibling_details = $xmlutils->get_sibling_details("foobar", 
																array('menuitemid'),
																array('label'));
	} catch (Exception $e) {
			assert_str_contains($expected_results,$e->getMessage(),
							$result_bool,$result_str);
	}
	
	output_results($result_bool,$result_str,$test);
}

function test_get_sibling_details_arg2_int($xmlutils) {

	$test="get siblings details - bad 2nd arg";
	$expected_results = "parameter must be array";
	
	$result_bool = false;
	
	try {
		$sibling_details = $xmlutils->get_sibling_details(3, 
																"foobar",
																array('label'));
	} catch (Exception $e) {
			assert_str_contains($expected_results,$e->getMessage(),
							$result_bool,$result_str);
	}
	
	output_results($result_bool,$result_str,$test);
}	

// ------------------------------------------------------------------
// children tests -------------------------------------------------
// ------------------------------------------------------------------

function test_get_children_details($xmlutils) {
	$test="get children - new style functions";
	$expected_array = array(array('menuitemid'=>3,'label' => 'theuppermiddle'),
									array('menuitemid'=>4,'label' => 'theuppermiddle'),
									array('menuitemid'=>5,'label' => 'theuppermiddle'),
									array('menuitemid'=>6,'label' => 'theuppermiddle'),
									array('menuitemid'=>'foobar','label' => 'theuppermiddle'));
													
	$child_details = $xmlutils->get_children_details(2, array('menuitemid'),
													array('label'));
	
	assert_arrays_equal($expected_array,$child_details,$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);	
}

function test_children_no_child() {
	$test="get children - no child";
	$result = "PASSED:".$test;
	$expected_array = array();
	
	//print_r($expected_array);
	
	$child_details = $xmlutils->get_child_details(5111,array('menuitemid'),
												array('label'));
	
	if ($child_details  != $expected_array) {
		$result = "FAILED:".$test;
	}
	echo $result."\n";
}

// ------------------------------------------------------------------
// item tests -------------------------------------------------------
// ------------------------------------------------------------------

function test_item($xmlutils) {
	$test="get item";
	$expected_result = true;
														
	$item = $xmlutils->get_item(5111);
	
	//if (!is_SimpleXMLElement($item) == true) {	}
	
	//print_r($item);	
	assert_true($expected_result,$xmlutils->is_SimpleXMLElement($item),
							$result_bool,$result_str);
	output_results($result_bool,$result_str,$test);	
}

// ------------------------------------------------------------------
// main -------------------------------------------------------------
// ------------------------------------------------------------------

$xmlutils = simplexml_load_string($xmlstr, 'XMLUtils');
$xmlutils->configure('menuitemid',1,'menuitem','menuitemid');

set_error_handler('\\XMLUtils::my_error_handler');

test_item_depth($xmlutils);
test_item_depth_root($xmlutils);

/* 
test_item($xmlutils);
test_get_sibling_details_arg1_int($xmlutils);
test_get_sibling_details_arg2_int($xmlutils);
test_get_sibling_details($xmlutils);
test_get_children_details($xmlutils);
test_get_ancestor_details($xmlutils);
test_item_details($xmlutils);
test_parent($xmlutils);
test_parent_bad_arg($xmlutils);
test_search($xmlutils);
test_search_int_as_string($xmlutils);
test_search_string($xmlutils);
test_search_top_item($xmlutils);
*/


?>