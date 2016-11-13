
<html>
<style>
label {
	display: inline-block;
	width:120px;
	text-alight=right;
}
</style>
</html>

<?php
$formdefn = <<<XML
<root>
	<dropdown id='1'>
		<field>Prep</field>
		<dbfield>prep</dbfield>
		<query>SELECT distinct(prep) FROM lesson</query>
		<value>5</value>
		<name>mySuggestion</name>
	</dropdown>
	<dropdown id='2'>
		<field>Student</field>
		<dbfield>name</dbfield>
		<query>SELECT name FROM student</query>
		<value>Peter</value>
		<name>mySuggestion1</name>
	</dropdown>
	
	<dropdown id='3'>
		<field>Adult</field>
		<dbfield>name</dbfield>
		<query>SELECT name FROM adult</query>
		<value>Amelia</value>
		<name>mySuggestion2</name>
	</dropdown>

</root>
XML;


set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
//set_include_path('/Users/burtnolej/Development/pythonapps/phpapps/utils');

include_once 'utils_xml.php';

function gettablecolumns($dbname,$tablename){

	$columns = array();
	
	$db = new SQLite3($dbname);
	
	$results = $db->query("pragma table_info(".$tablename.")");
	
	while ($row = $results->fetchArray()) {
		if (substr($row[1],0,2) <> "__") {
			$columns[] = $row[1];
		}
	}
	
	return($columns);
}
function get_htmldbdropdown($column,$values,$widgetcount) {

	$datalistname = "suggestions".$widgetcount;

	echo "<label for=\"".$column."\" >".$column."</label>";
	echo "<input type=\"text\" id=\"".$column."\" list=\"".$datalistname."\" />";
	echo "<datalist id=\"".$datalistname."\">";
	
	foreach ($values as $value) {
			echo "<option>".$value."</option>";
		}
		
	echo "</datalist>";
}

function getcolumndistinctvalues($dbname,$tablename,$colname) {
		
	$values = array();
	
	$db = new SQLite3($dbname);
	
	$results = $db->query("select distinct(".$colname.") from ".$tablename);
	
	while ($row = $results->fetchArray()) {
		$values[] = $row[0];
	}
	
	return $values;
}

$columns = gettablecolumns("test.sqlite","lesson");

$widgetcount=0;
foreach ($columns as $column) {
	
	echo "<div class=\"container\">	";
	
	$values = getcolumndistinctvalues("test.sqlite","lesson",$column);

	get_htmldbdropdown($column,$values,$widgetcount);
	
	$widgetcount = $widgetcount+1;
	

	echo "</div>";
}

?>

