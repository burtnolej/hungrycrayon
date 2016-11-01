<?php
$xmlstr = <<<XML
<root>
	<row id='1'>
		<cell id = '1.1'>
			<value>foo</value>
			<fgcolor>FF0FFF</fgcolor>
			<bgcolor>FF00FF</bgcolor>
		</cell>
	</row>
	<row id='2'>
		<cell id = '2.1'>
			<value>bar</value>
			<fgcolor>FFFFFF</fgcolor>
			<bgcolor>FF0000</bgcolor>
		</cell>
	</row>
</root>
XML;

include_once '../utils/utils_xml.php';
include_once '../utils/utils_error.php';
include_once '../utils/utils_test.php';

set_error_handler('\\UtilsError::error_handler');

$gridarr = Array(); // declare resulting array

// load xml string into XML Utils
$utilsxml = simplexml_load_string($xmlstr, 'utils_xml');		

// get a list of all rows
$_rows = $utilsxml->xpath("//row");

echo "<table border='1' style=width:100%>";

foreach ($_rows as $_row) {
	
	echo "<tr>";
	
	// get a list of the cells (children) of this row
	$_cells = $_row->xpath("child::*");
	
	foreach ($_cells as $_cell) {

		echo "<td";
		echo " bgcolor=#".$_cell->bgcolor;
		echo " fgcolor=#".$_cell->fgcolor;
		echo ">";
		echo $_cell->value;
		echo "</td>";
	}
	echo "</tr>";
}
echo "</table> ";
