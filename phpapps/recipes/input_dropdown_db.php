
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
		<value>Peter</value>
	</dropdown>
</root>
XML;

set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
include_once 'utils_xml.php';

function get_htmldbdropdown($dbname,$xmlformdefn) {
	
	$db = new SQLite3($dbname);
	
	$utilsxml = simplexml_load_string($xmlformdefn, 'utils_xml');	

	$_dropdowns = $utilsxml->xpath("//dropdown");

	foreach ($_dropdowns as $_dropdown) {

		echo "<label for=\".$field.\">".$_dropdown->field."</label>";
		echo "<input type=\"text\" id=\"".$_dropdown->field."\" list=\"mySuggestion\" />";
		echo "<datalist id=\"mySuggestion\">";

		$results = $db->query($_dropdown->query);
		while ($row = $results->fetchArray()) {
			foreach ($row as $value) {
				echo "<option ";
  				if ($value == $_dropdown->value) {
  					echo "selected=\"selected\"";
  				}
  				echo ">".$value."</option>";
			}
		}
		echo "</datalist>";
	}
}
get_htmldbdropdown("test.sqlite",$formdefn);

?>

