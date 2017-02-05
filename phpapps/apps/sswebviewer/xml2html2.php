

<?php

$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);

include_once 'utils_xml.php';
include_once 'ui_utils.php';

function getlinkurl($cell,$args,$page='dpivot.php') {
	
		$url = $page."?source_type=".$cell->valuetype."&source_value=".$cell->value;
		
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
			//drawcell($_subcells[$i],"cell sub",$args,sizeof($_subcells)-1,$i);
			drawcell($_subcells[$i],"thincol borderoff",$args,sizeof($_subcells)-1,$i);
			//echo "<tr><td class=\"thincol borderoff\" bgcolor=\"#E0E0E0\"";
			
		}
		echo "</tr>";
	}
}

function drawgrid($utilsxml,$args=NULL,$formats=NULL) {
	
	$_rows = $utilsxml->xpath("//row"); // get a list of all rows
	
	//echo "<table id=table >";
	echo "<table class = \"borderoff\"";
	
	if (isset($args['id'])) {
		echo " id =\"".$args['id']."\"";
	}
	
	echo ">";

	if (isset($args['headeronly'])) {
		$_rows = Array($_rows[0]);
	}
	
	if (isset($args['noheader'])) {
		unset($_rows[0]);
	}

	foreach ($_rows as $_row) {
	
		echo "<tr>"; // start an html row
		$_cells = $_row->xpath("child::*"); // get a list of the cells (children) of this row
	
		foreach ($_cells as $_cell) {
			
			$_subrows = $_cell->xpath("child::subrow"); // see if any subrows exist
			
			if (sizeof($_subrows) <> 0) {

				//echo '<td><table class="table sub">'; // start a new table
				echo "<td><table class = \"borderoff\">";
				
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

	
	
	echo "<table class = \"borderoff\">";

	$_rows = $utilsxml->xpath("//row"); // get a list of all rows
	
	foreach ($_rows as $_row) {
	
		echo "<tr>"; // start an html row
		$_cells = $_row->xpath("child::*"); // get a list of the cells (children) of this row
	
		foreach ($_cells as $_cell) {
			echo "<td>";
			
			$_subrows = $_cell->xpath("child::subrow"); // see if any subrows exist
			
			if (sizeof($_subrows) <> 0) {
				 echo "<table class = \"borderoff\">"; // start a new table

				foreach ($_subrows as $_subrow) {	

					echo "<tr><td class=\"thincol borderoff\" bgcolor=\"#E0E0E0\"";

					$content="";	
					$_subcells = $_subrow->xpath("child::subcell"); // see if any subcells exist
	
					if (sizeof($_subcells) <> 0) {
						
						for ($i=0;$i<sizeof($_subcells);$i++) {
							$url = getlinkurl($_subcells[$i],$args);
							
							$output = array();
							
							echo "inhere";
							
							if ($_subcells[$i]->valuetype == 'adult') {
								$link = '<a href="'.$url.'">'."<font color=\"darkred\">".$_subcells[$i]->value."</font>".'</a>';
								$content =$content." with ".$link;
							}
							elseif ($_subcells[$i]->valuetype == 'student') {
								$link = '<a href="'.$url.'">'.$_subcells[$i]->value.'</a>';
								$content = $content." [".$link."] ";
							}
							elseif ($_subcells[$i]->valuetype == 'subject') {
								$link = '<a href="'.$url.'">'."<font color=\"darkgreen\">".$_subcells[$i]->value."</font>".'</a>';
								//$link = '<a href="'.$url.'">'.$_subcells[$i]->value.'</a>';
								$content = $content.$link;
							}
							elseif ($_subcells[$i]->valuetype == 'period') {
								$link = '<a href="'.$url.'">'."<font color=\"orange\">".$_subcells[$i]->value."</font>".'</a>';
								$content = $content." @".$link;
							}
							elseif ($_subcells[$i]->valuetype == 'dow') {
								$link = '<a href="'.$url.'">'."<font color=\"purple\">".$_subcells[$i]->value."</font>".'</a>';
								$content = $content." on ".$link;
							}
							elseif ($_subcells[$i]->valuetype == 'recordtype') {
								$link = '<a href="'.$url.'">'."<font color=\"darkblue\">".$_subcells[$i]->value."</font>".'</a>';
								//$link = '<a href="'.$url.'">'.$_subcells[$i]->value.'</a>';
								$content = $content." {".$link."} ";
							}
							elseif ($_subcells[$i]->valuetype == 'id') {
								$url = getlinkurl($_subcells[$i],$args,"dedit.php");
								$link = '<a href="'.$url.'">'."<i>".$_subcells[$i]->value."</i>".'</a>';
								//$link = '<a href="'.$url.'">'.$_subcells[$i]->value.'</a>';
								$content = $content." {".$link."} ";
							}
							else {
								$link = '<a href="'.$url.'">'.$_subcells[$i]->value.'</a>';
								$content = $content.$link;
								//echo $_subcells[$i]->valuetype;
							}

							
						}
						echo ">".$content;
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
	
function drawmultirecordform($utilsxml,$args=NULL,$formats=NULL) {
	
	echo "<div class=\"tmp\";><br>";
	
	$_records = $utilsxml->xpath("//record"); // get all the records
	
	foreach ($_records as $_record) {
		
			$func = function() use ($_record) {
				
					global $SSDB;
					
				 	$_items = $_record->xpath("./item"); // get a list of all rows
				 
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
		
						$values = getcolumndistinctvalues($SSDB,'lesson',$valuetype);
		
						array_splice($values,0,0,"NotSelected");
						array_splice($values,1,0,"all");
						
						getchtmlselect_nolabel($valuetype,$values,$widgetcount,$_item->value,$comment);
					}	
			};
			
			gethtmldiv("",$func,"blank",NULL);		
	}
	
	echo "</div>";
}

function drawform($utilsxml,$args=NULL,$formats=NULL) {

	$func = function() use ($utilsxml) {
					
		$_items = $utilsxml->xpath("./item"); // get a list of all rows
   
   		$widgetcount=0;
		foreach ($_items as $_item) {
	
			if ($_item->valuetype == 'adult') {
    			$valuetype='teacher'; ## needs to be enabled if distinct enabled below
				//$valuetype='adult';
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
				
			global $SSDB;
			
			//getchtmldbselect($SSDB,"lesson",$valuetype,$valuetype,$widgetcount,$_item->value,NULL,"comment");
			getchtmldbselect($SSDB,"lesson",$_item->valuetype,$valuetype,$widgetcount,$_item->value,array("distinct" => false));

			$widgetcount=$widgetcount+1;
		   }
	};

	gethtmldiv("select something",$func,"contain",NULL);		
}

function drawentryform($utilsxml,$args=NULL,$formats=NULL) {

	$func = function() use ($utilsxml) {
		$_items = $utilsxml->xpath("./item"); // get a list of all rows
   
   		$widgetcount=0;
		foreach ($_items as $_item) {
					
			global $SSDB;
			getchtmlinput($_item->valuetype,$_item->valuetype,$_item->value,NULL);
			$widgetcount=$widgetcount+1;
		   }
	};

	gethtmldiv("input something",$func,"contain",NULL);		
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
	
	//$args = Array('headeronly' => true,'id' => 'table1');
	call_user_func((string)$funcname,$utilsxml,$args,$formats);
	//$args = Array('noheader' => true,'id' => 'table2');
	//call_user_func((string)$funcname,$utilsxml,$args,$formats);
	
}	
	
