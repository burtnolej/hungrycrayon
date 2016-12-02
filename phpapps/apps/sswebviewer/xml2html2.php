<html>
<link rel="stylesheet" type="text/css" href="default.css" />
</html>

<?php

$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);

include_once 'utils_xml.php';
include_once 'ui_utils.php';

function getlinkurl($cell,$args) {
	
		$url = "dpivot.php?source_type=".$cell->valuetype."&source_value=".$cell->value;
		
		if ($args<>NULL) {
		
			$url = $url."&xaxis=".$args['xaxis']."&yaxis=".$args['yaxis'];
		
			if (is_array($args['ztypes']) == True) {
				$url = $url."&ztypes=".implode(",",$args['ztypes']);
			}
			else {
				$url = $url."&ztypes=".$args['ztypes'];
			}
		}
		return $url;
}

function drawcell($cell,$class,$args,$size=1,$index=1) {
	// size describes how many cells there are on this row
	// index describes which cell this is, so correct class can be assigned

	if (isset($cell->type)) {
		$class = $class." ".$cell->type;
	}
	else {
		if ($class == "cell sub") {
			switch($index){
				case 0:
					$class = $class." left";
					break;
				case $size:
					$class = $class." right";
					break;
				default:
					$class = $class." middle";
					break;
			}
		}	
	}
	
	echo "<td class=\"".$class."\"";
	
	if (isset($cell->bgcolor)) {
		echo " bgcolor=".$cell->bgcolor;
	}
	
	if (isset($cell->fgcolor)) {	
		echo " fgcolor=".$cell->fgcolor;
	}
	
	if (isset($cell->shrinkfont)) {
		if (strlen($cell->value) > $cell->shrinkfont) {
			$zoom= round((6 / strlen($cell->value)) * 100);
			echo " style=\"font-size: ".$zoom."%;\"";
		}
	}
	
	echo ">";

	if (isset($cell->valuetype)) {
		
		$url = getlinkurl($cell,$args);
		echo '<a href="'.$url.'">'.$cell->value.'</a>';
	}
	else {
		// no formats just plain cell from a 2d grid. assumes no value attr set so takes text
		// value of the cell object
		echo $cell[0];
	}
	echo "</td>";
} 

function drawrow($row,$args) {
	echo "<tr>"; // start a sub row
				
	$_subcells = $row->xpath("child::subcell"); // see if any subcells exist
	
	if (sizeof($_subcells) <> 0) {
		for ($i=0;$i<sizeof($_subcells);$i++) {
			drawcell($_subcells[$i],"cell sub",$args,sizeof($_subcells)-1,$i);
		}
		echo "</tr>";
	}
}

function drawgrid($utilsxml,$args=NULL,$formats=NULL) {
	
	echo "<table id=table >";

	$_rows = $utilsxml->xpath("//row"); // get a list of all rows

	foreach ($_rows as $_row) {
	
		echo "<tr>"; // start an html row
		$_cells = $_row->xpath("child::*"); // get a list of the cells (children) of this row
	
		foreach ($_cells as $_cell) {
			
			$_subrows = $_cell->xpath("child::subrow"); // see if any subrows exist
			
			if (sizeof($_subrows) <> 0) {

				echo '<td><table class="table sub">'; // start a new table

				foreach ($_subrows as $_subrow) {					
					drawrow($_subrow,$args);
				}
				echo "</table></td>";
			}
			else {
				$_subcells = $_cell->xpath("child::subcell"); // see if any subcells exist
	
				if (sizeof($_subcells) <> 0) { // subcells no subrows
					echo '<td><table class="table sub">'; // start a new table
					drawrow($_cell,$args);
					echo "</table></td>";
				}
				else { // no subcells or subrows so create a regular cell
					drawcell($_cell,"cell",$args);
				}
			}	
		}
		echo "</tr>";
	}
	echo "</table> ";
}

function drawnoformatgrid($utilsxml,$args=NULL,$formats=NULL) {
	
	if ($args['yaxis'] == "adult") {
		echo "<table class = \"\">";
	}
	else {
		echo "<table class = \"widecolumns\">";
	}
	

	$_rows = $utilsxml->xpath("//row"); // get a list of all rows

	foreach ($_rows as $_row) {
	
		echo "<tr>"; // start an html row
		$_cells = $_row->xpath("child::*"); // get a list of the cells (children) of this row
	
		foreach ($_cells as $_cell) {
			echo "<td id=\"\">";
			
			$_subrows = $_cell->xpath("child::subrow"); // see if any subrows exist
			
			if (sizeof($_subrows) <> 0) {
				 echo "<table class = \"sub\">"; // start a new table

				foreach ($_subrows as $_subrow) {	
	
					if ($args['yaxis'] == "adult") {
						echo "<tr><td class=\"sub\">";
					}
					else {						
						echo "<tr><td class=\"sub widecolumns\">";
					}
					$content="";	
					$_subcells = $_subrow->xpath("child::subcell"); // see if any subcells exist
	
					if (sizeof($_subcells) <> 0) {
						
						for ($i=0;$i<sizeof($_subcells);$i++) {
							$url = getlinkurl($_subcells[$i],$args);
							$link = '<a href="'.$url.'">'.$_subcells[$i]->value.'</a>';
							if ($_subcells[$i]->valuetype == 'adult') {
								$content = $content." with ".$link;
							}
							elseif ($_subcells[$i]->valuetype == 'student') {
								//$content = $content." [".$_subcells[$i]->value."] ";
								$content = $content." [".$link."] ";
							}
							else {
								//$content = $content.$_subcells[$i]->value;
								$content = $content.$link;
							}
							
						}
						echo $content;
					}
					echo "</td></tr>";					
				}
				echo "</table></td>";
			}
			else {
				$content = $_cell->value;
				echo $content;
			}
		}
		echo "</td>";
		echo "</tr>";
	}
	echo "</table> ";
}


function drawform($utilsxml,$args=NULL,$formats=NULL) {

   echo "<html><body>";
   echo '<form action="update.php" method="post" accept-charset="UTF-8">';
   echo "<fieldset>";

	$_items = $utilsxml->xpath("//item"); // get a list of all rows
   
   $widgetcount=0;
	foreach ($_items as $_item) {
	
		if ($_item->valuetype == 'adult') {
    		$valuetype='teacher';
    	}
    	elseif ($_item->valuetype == 'id') {
	 		$valuetype='__id';
	 	}
    	elseif ($_item->valuetype == 'objtype') {
	 		continue;
	 	}
      else {
        	$valuetype=$_item->valuetype;
		}

   	gethtmltablecoldropdown('test.sqlite','lesson',$valuetype,$widgetcount,$_item->value);
   	$widgetcount=$widgetcount+1;
	}
	
   echo "</fieldset>";
   echo "</form>";
   echo "</body></html>";
}

function draw($xmlstr,$args=NULL) {
		
	// load xml string into XML Utils
	$utilsxml = simplexml_load_string($xmlstr, 'utils_xml');	
	
	$_parser = $utilsxml->xpath("//parser"); // get parser
	
	// check if formats is selected
	$formats=NULL;
	$ztypes_array = explode(",",$args['ztypes']);
	if (in_array("formats",$ztypes_array)) {
		$formats=TRUE;
	}
	
	if (sizeof($_parser) <> 0) {
		$_item =$_parser[0]; 
		$funcname = $_item->value;
		
	}
	else {
		$funcname = 'drawgrid';
	}
	
	call_user_func((string)$funcname,$utilsxml,$args,$formats);
	
}	
	
