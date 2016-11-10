
<html>
<style>
label {
	display: inline-block;
	width:70px;
	text-alight=right;
}
</style>
</html>

<?php
$formdefn = <<<XML
<root>
	<dropdown id='1'>
		<field>Student</field>
		<query>SELECT name FROM student</query>
		<value>Peter</value>
	</dropdown>
	<dropdown id='2'>
		<field>Adult</field>
		<query>SELECT name FROM adult</query>
		<value>Amelia</value>
	</dropdown>
</root>
XML;



//set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
set_include_path('/Users/burtnolej/Development/pythonapps/phpapps/utils');

include_once 'utils_xml.php';

function get_htmldbdropdown($dbname,$xmlformdefn) {
	
	$db = new SQLite3($dbname);
	
	$utilsxml = simplexml_load_string($xmlformdefn, 'utils_xml');	

	$_dropdowns = $utilsxml->xpath("//dropdown");

	foreach ($_dropdowns as $_dropdown) {

		echo "<div>";
		echo "<label for=\"".$_dropdown->field."\" >".$_dropdown->field."</label>";
		echo "<input type=\"text\" value=\"".$_dropdown->value."\" id=\"".$_dropdown->field."\" list=\"".$_dropdown->field."\" />";
		echo "<datalist id=\"".$_dropdown->field."\">";

		$results = $db->query($_dropdown->query);
		while ($row = $results->fetchArray()) {
			foreach ($row as $value) {
				echo "<option>".$value."</option>";
			}
		}
		echo "</datalist>";
		echo "</div>";
	}
}
get_htmldbdropdown("test.sqlite",$formdefn);

?>

