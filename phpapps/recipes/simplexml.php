<?php

$xmlstr = <<<XML
<menu>
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

//include 'samplexml.php';
include 'xml_utils.php';

$xmlutils = simplexml_load_string($xmlstr, 'XMLUtils');
$xmlutils->configure('label','root','menuitem','menuitemid');

// --------------------------------------------
// --------------------------------------------
$test="search tree for specific item";
$result = "PASSED:".$test;
$expected_label = 'thelowermiddle-sibling1';

$item = $xmlutils->get_menuitem(4);

if ($item->label != $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

$test="search tree for specific item passing in xpath_expr";
$result = "PASSED:".$test;
$expected_label = 'thelowermiddle-sibling1';

$item = $xmlutils->get_menuitem(4);

if ($item->label != $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";
// --------------------------------------------
// --------------------------------------------
$test="get label of parent node";
$result = "PASSED:".$test;
$expected_label = 'thelowermiddle';

// Test 1
$item = $xmlutils->get_menuitem(31);
$parent_label = $xmlutils->get_parent($item);

if ($parent_label == $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// Test 2
$test="et label of parent node from menuid";
$result = "PASSED:".$test;

$parent_label = $xmlutils->get_parent(31);

if ($parent_label == $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get siblings of node";
$result = "PASSED:".$test;
$expected_results = array('thelowermiddle','thelowermiddle-sibling1',
						'thelowermiddle-sibling2','thelowermiddle-sibling3',
						'foobar-sibling');

//$xml = new SimpleXMLElement($xmlstr_siblings);

// Test 1
$item = $xmlutils->get_menuitem(3);
$siblings = $xmlutils->get_siblings($item);

if ($siblings != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// Test 2
$test="get siblings of node from menuid";
$result = "PASSED:".$test;
$siblings = $xmlutils->get_siblings(3);

if ($siblings != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get all ancestors of node";
$result = "PASSED:".$test;
$expected_results = array('thelowermiddle-sibling1','theuppermiddle','root');

// Test 1
$item = $xmlutils->get_menuitem(41);
$ancestors=$xmlutils->get_ancestors($item);

if ($ancestors != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// Test 2
$test="get all ancestors of node from menuid";
$result = "PASSED:".$test;
$ancestors=$xmlutils->get_ancestors(41);

if ($ancestors != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get all details of node";
$result = "PASSED:".$test;
$expected_results = array('tag' => 'foobar','label'=>'thelowermiddle');

$details = $xmlutils->get_menuitem_details(31,array('tag'),array('label'));

if ($details != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get depth of node";
$result = "PASSED:".$test;
$expected_results = 3;

$depth = $xmlutils->get_menuitem_depth(41);

if ($depth != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="search tree for specific item - int as a string";
$result = "PASSED:".$test;
$expected_label = 'thelowermiddle-sibling1';

$item = $xmlutils->get_menuitem('4');

if ($item->label != $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="search tree for specific item - string";
$result = "PASSED:".$test;
$expected_label = 'foobar-sibling';

$item = $xmlutils->get_menuitem('foobar');

if ($item->label != $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="search tree for top item";
$result = "PASSED:".$test;
$expected_label = 'theuppermiddle';

$item = $xmlutils->get_menuitem(2);

if ($item->label != $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";
// --------------------------------------------
// --------------------------------------------
$test="get children";
$result = "PASSED:".$test;
$expected_array = array(array('label' => 'theuppermiddle','menuitemid'=>3),
								array('label' => 'theuppermiddle','menuitemid'=>4),
								array('label' => 'theuppermiddle','menuitemid'=>5),
								array('label' => 'theuppermiddle','menuitemid'=>6),
								array('label' => 'theuppermiddle','menuitemid'=>'foobar'));


//print_r($expected_array);

$child_details = $xmlutils->get_child_details(2,array('menuitemid'),
											array('label'));

if ($child_details  != $expected_array) {
	$result = "FAILED:".$test;
}
echo $result."\n";
// --------------------------------------------
// --------------------------------------------
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
?>