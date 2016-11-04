<html>
<style>

#cell {
    padding:0px;
    line-height:30px;
    background-color:#eeeeee;
    //<!height:2000px;>
    float:left;
    text-align:center;;
    border: 1px solid #73AD21;
}

#rowhdrcell {
    padding:0px;
    line-height:30px;
    foreground-color:#D0C978;
    background-color:#98969B;
    <!height:2000px;>
    float:left;
    text-align:center;;
    width: 50px;
    border: 1px solid #73AD21;
}

#table {
	width:100%;
   background-color:#eeeeee;
   	<!height:2000px;>
   float:left;
   text-align:center;;
}

table {
    border-collapse: collapse;
}

</style>
</html>

<?php

include_once '../../utils/utils_xml.php';

function drawcell($cell) {
	
	if (isset($cell->type)) {
		echo "<td id=".$cell->type;
	}
	else {
		echo "<td id=cell";
	}
	
	if (isset($cell->bgcolor)) {
		echo " bgcolor=#".$cell->bgcolor;
	}
	
	if (isset($cell->fgcolor)) {	
		echo " fgcolor=#".$cell->fgcolor;
	}
	
	echo ">";
	echo $cell->value;
	echo "</td>";
} 

function drawgrid($xmlstr) {
	
	echo "<table id=table >";
	
	// load xml string into XML Utils
	$utilsxml = simplexml_load_string($xmlstr, 'utils_xml');	

	// get a list of all rows
	$_rows = $utilsxml->xpath("//row");

	foreach ($_rows as $_row) {
	
		echo "<tr>"; // start an html row
		$_cells = $_row->xpath("child::*"); // get a list of the cells (children) of this row
	
		foreach ($_cells as $_cell) {
		
			$_subcells = $_cell->xpath("child::subcell"); // see if any subcells exist
	
			if (sizeof($_subcells) <> 0) {
			
					echo "<td>";
					echo "<table id=table>"; // start a new table
					echo "<tr>"; // all subcells go on one row
				
					foreach ($_subcells as $_subcell) {
							drawcell($_subcell);
					}
					echo "</tr>";
					echo "</table>";
					echo "</td>";
			}
			else { // create a regular cell
				drawcell($_cell);
			}
		}
		echo "</tr>";
	}
	echo "</table> ";
}