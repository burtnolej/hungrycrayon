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
		</menuitem>
		<menuitem>
			<menuitemid>6</menuitemid>
			<label>thelowermiddle-sibling3</label>
		</menuitem>
	</menuitem>
</menu>
XML;

//include 'samplexml.php';
include 'xml_utils.php';

$xml = new SimpleXMLElement($xmlstr);

// --------------------------------------------
// --------------------------------------------
$test="search tree for specific item";
$result = "PASSED:".$test;
$expected_label = 'thelowermiddle-sibling1';

$item = get_menuitem($xml,4);

if ($item->label != $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

$test="search tree for specific item passing in xpath_expr";
$result = "PASSED:".$test;
$expected_label = 'thelowermiddle-sibling1';

$item = get_menuitem($xml,4,'menuitem','menuitemid');

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
$item = get_menuitem($xml,31);
$parent_label = get_parent($item);

if ($parent_label == $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// Test 2
$test="et label of parent node from menuid";
$result = "PASSED:".$test;

$parent_label = get_parent(31,$xml);

if ($parent_label == $expected_label) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get siblings of node";
$result = "PASSED:".$test;
$expected_results = array('thelowermiddle','thelowermiddle-sibling1','thelowermiddle-sibling2','thelowermiddle-sibling3');

//$xml = new SimpleXMLElement($xmlstr_siblings);

// Test 1
$item = get_menuitem($xml ,3);
$siblings = get_siblings($item);

if ($siblings != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// Test 2
$test="get siblings of node from menuid";
$result = "PASSED:".$test;
$siblings = get_siblings(3,$xml);

if ($siblings != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get all ancestors of node";
$result = "PASSED:".$test;
$expected_results = array('thelowermiddle-sibling1','theuppermiddle','root');

//$xml = new SimpleXMLElement($xmlstr_siblings);

// Test 1
$item = get_menuitem($xml,41);
$ancestors=get_ancestors($item,'root');

if ($ancestors != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// Test 2
$test="get all ancestors of node from menuid";
$result = "PASSED:".$test;
$ancestors=get_ancestors(41,'root',$xml);

if ($ancestors != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get all details of node";
$result = "PASSED:".$test;
$expected_results = array('tag' => 'foobar','label'=>'thelowermiddle');

$details = get_menuitem_details($xml,31,array('tag'),array('label'));

if ($details != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

// --------------------------------------------
// --------------------------------------------
$test="get depth of node";
$result = "PASSED:".$test;
$expected_results = 3;

$depth = get_menuitem_depth($xml,41,'label','root');

if ($depth != $expected_results) {
	$result = "FAILED:".$test;
}
echo $result."\n";

?>
