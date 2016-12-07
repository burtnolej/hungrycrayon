
<?php

$PHPLIBPATH = getenv("PHPLIBPATH");
$SSDBPATH = getenv("SSDBPATH");
set_include_path($PHPLIBPATH);

//set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
include_once 'db_utils.php';
include_once 'utils_xml.php';

// HTML Label
function gethtmllabel($label, $labelclass=NULL) {

	echo "<label for=".$label;
	if ($labelclass <> NULL) {
		echo " class =\"".$labelclass."\"";
	}

	echo ">".$label."</label>";

}

// HTML Dropdown
function gethtmldropdown($column,$values,$widgetcount,$default=NULL) {

	$datalistname = "suggestions".$widgetcount;

	echo "<label for=\"".$column."\" >".$column."</label>";
	//echo "<input type=\"text\" name=\"".$column."\" id=\"".$column."\" list=\"".$datalistname."\" autocomplete=\"off\" ";
	echo "<input type=\"text\" name=\"".$column."\" id=\"".$column."\" list=\"".$datalistname."\""; 

	if (isset($default) and $default <> "") {
		echo " value=\"".$default."\"";
	}	
	
	echo ">";
	echo "<datalist id=\"".$datalistname."\">";
	
	foreach ($values as $value) {
			echo "<option>".$value."</option>";
		}
		
	echo "</datalist>";
}

// HTML Select
function gethtmlselect($column,$values,$widgetcount,$default, $label=NULL,$labelclass=NULL,$spanclass=NULL,$class=NULL) {

	echo "<span ";
	if ($spanclass <> NULL) {
			echo "class =\"".$spanclass."\"";
	}
	echo ">";
	
	if ($label <> FALSE ) {
		gethtmllabel($label,$labelclass);
	}
	
	echo "<select ";
	if ($class <> NULL) {
			echo "class =\"".$class."\" ";
	}

	echo "id=\"".$column."\" name=\"".$column."\">"; 
	
	foreach ($values as $value) {
			echo "<option value=\"".$value."\"";
			
			if ($value == $default) {
			//if ($value == $defaults[$column]) {
				echo "selected";
			}	
	
			echo ">".$value."</option>";
		}
		
	echo "</select>";
	echo "</span>";

}
		
// Custom HTML Select
function getchtmlselect($column,$values,$widgetcount,$default,$comment=NULL) {

	echo "<p class=\"label\">".$column."</p>";
	echo "<span class=\"select\">";		
	echo "<select class=\"custom\" id=\"".$column."\" name=\"".$column."\">"; 
	
	foreach ($values as $value) {
			echo "<option value=\"".$value."\"";
			if ($value == $default) {
				echo "selected";
			}	
			echo ">".$value."</option>";
		}
		
	echo "</select>";
	echo "</span>";
	if ($comment <> NULL) {
		echo "<p class=\"comment\">".$comment."</p>";
	}
}

// HTML DB Dropdown
function gethtmldbdropdown($dbname,$tablename){
	
	$columns = gettablecolumns($dbname,$tablename);
		
	$widgetcount=0;

	foreach ($columns as $column) {
	
		echo "<div class=\"container\">";
		
		$values = getcolumndistinctvalues($dbname,$tablename,$column);

		gethtmldropdown($column,$values,$widgetcount);
	
		$widgetcount = $widgetcount+1;
	
		echo "</div>";
	}
}

// HTML DB Select
function gethtmldbselect($dbname,$tablename,$column,$name,$widgetcount,$default,$labels=FALSE,$labelclass=FALSE,$spanclass=NULL,$class=NULL){
			
	$values = getcolumndistinctvalues($dbname,$tablename,$column);

	array_splice($values,0,0,"NotSelected");
	array_splice($values,1,1,"all");
	
	if ($labels == TRUE) {
		gethtmlselect($name,$values,$widgetcount,$default,$column,$labelclass,$spanclass,$class);
	}
	else{
		gethtmlselect($name,$values,$widgetcount,$default,$labels,$labelclass,$spanclass,$class);
	}
}

// Custom HTML DB Select
function getchtmldbselect($dbname,$tablename,$column,$name,$widgetcount,$default,$divlabel="",$comment=NULL){
			
	if ($divlabel<>NULL) {
		echo "<div class=\"contain\">";
		echo "<p class=\"divlabel\">".$divlabel."</p>";
	}
	
	$values = getcolumndistinctvalues($dbname,$tablename,$column);

	array_splice($values,0,0,"NotSelected");
	array_splice($values,1,1,"all");
	
	getchtmlselect($name,$values,$widgetcount,$default,$comment);
	
	if ($divlabel<>NULL) {
		echo "</div>";
	}
}

// Custom HTML XML Select
function getxmlhtmlcselect($xml,$defaults,$divlabel) {
	
	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
	$_dropdowns = $utilsxml->xpath("//select");
	
	$widgetcount = 0;
	
	echo "<div class=\"contain\">";
	echo "<p class=\"divlabel\">".$divlabel."</p>";
		
	foreach ($_dropdowns as $_dropdown) {
				
		$values = $_dropdown->values->xpath("child::value");
		$field = (string)$_dropdown->field;
		$default = NULL;

		if (array_key_exists($field,$defaults)) {
			$default = $defaults[$field];
		}
		elseif (isset($_dropdown->default)){
			$default = (string)$_dropdown->default;			
		}

		getchtmlselect($field,$values,$widgetcount,$default,(string)$_dropdown->comment);
		
		$widgetcount = $widgetcount+1;
	}
	echo "</div>";
}

// HTML XML Select
function gethtmlxmlselect($xml,$defaults,$labels=FALSE,$labelclass=FALSE,$spanclass=NULL,$class=NULL) {
	
	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
	$_dropdowns = $utilsxml->xpath("//select");
	
	$widgetcount = 0;

	foreach ($_dropdowns as $_dropdown) {
				
		$values = $_dropdown->values->xpath("child::value");
		$field = (string)$_dropdown->field;
		$default = NULL;

		if (array_key_exists($field,$defaults)) {
			$default = $defaults[$field];
		}
		elseif (isset($_dropdown->default)){
			$default = (string)$_dropdown->default;			
		}
		
		if ($labels == TRUE) {
			gethtmlselect($field,$values,$widgetcount,$default,$field,$labelclass,$spanclass,$class);
		}
		else {
			gethtmlselect($field,$values,$widgetcount,$default,$labels,$labelclass,$spanclass,$class);
		}
		
		echo "<br><br>";
		
		$widgetcount = $widgetcount+1;
	}
}

// HTML DB Table Column Dropdown
function gethtmltablecoldropdown($dbname,$tablename,$column,$widgetcount,$default=NULL){
	
	echo "<div class=\"container\">";
		
	$values = getcolumndistinctvalues($dbname,$tablename,$column);

	gethtmldropdown($column,$values,$widgetcount,$default);
	
	$widgetcount = $widgetcount+1;
	
	echo "</div>";

}

// HTML XML Dropdown
function gethtmlxmldropdown($xml) {
	
	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
	$_dropdowns = $utilsxml->xpath("//dropdown");
	
	$widgetcount = 0;
	
	foreach ($_dropdowns as $_dropdown) {
			
		echo "<div class=\"container\">";

		$values = $_dropdown->values->xpath("child::value");

		if (!isset($_dropdown->default)){
			$_dropdown->default = NULL;
		}
		gethtmldropdown($_dropdown->field,$values,$widgetcount,$_dropdown->default);

		$widgetcount = $widgetcount+1;
	
		echo "</div>";
	}
}

// HTML Button
function gethtmlbutton($type,$label) {
	
	echo "<input type=\"".$type."\" name=\"".$type."\" value=\"".$label."\" />";

}

// HTML DB Checkbox
function getdbhtmlmultiselect($dbname,$query,$name,$maxy=0,$checked=NULL) {
	
		$db = new SQLite3($dbname);

		$results = $db->query($query);
		
		echo "<table><tr>";
		$ycount=0;
		while ($row = $results->fetchArray()) {
				if ($ycount>$maxy) {
					echo "</tr><tr>";
					$ycount=0;
				}
				echo "<td>";
				gethtmlmultiselect($name,$row['name'],$checked);
				echo "</td>";
				$ycount=$ycount+1;
		}
		echo "</tr></table>";
}

// HTML Checkbox
function gethtmlmultiselect($name,$value,$checked=NULL) {
	
		echo "<input id=\"".$value."\" type=\"checkbox\" name=\"".$name."[]\" value=\"".$value."\"";
		
		if (isset($checked)) {
			if (in_array($value,$checked)) {
				
				echo "checked";
			}
		}
		echo "/>";
		echo "<label for=\"".$value."\" >".$value."</label>";

}

// HTML switch/slider
function gethtmlswitch($name,$value,$checked=NULL) {

		echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"switch.css\" />";
		echo "<label class=\"switch\">";
		
		echo "<input id=\"".$value."\" type=\"checkbox\" name=\"".$name."\"";

		if (isset($checked)) {
			if (in_array($value,$checked)) {
				echo "checked";
			}
		}
		
		echo ">";
		echo "<div class=\"slider\"></div>";
		echo "</label>";
}

// Custom HTML switch/slider
function getchtmlswitch($name,$value,$checked=NULL) {

		echo "<p class=\"label switch\">".$name."</p>";
		echo "<label class=\"switch\">";
		
		echo "<input id=\"".$value."\" type=\"checkbox\" name=\"".$name."\"";

		if (isset($checked)) {
			if (in_array($value,$checked)) {
				echo "checked";
			}
		}
		
		echo ">";
		echo "<p class=\"slider\"></p>";
		echo "</label>";
}

function _menu_iter($func,$root,$depth){

	if ($depth==0) {
		echo '<ul class = "nav">';	
	}
	else {
		echo "<ul>";
	}
	
	foreach ($root as $tag => $node) {
		
		echo "<li>";
		
		$func($tag,$node);

		$xpath_str = sprintf("./%s","item");
		$items = $node->xpath($xpath_str);

		if (sizeof($items)<> 0) {
			
			$depth+=1;
			_menu_iter($func,$node,$depth);
		}
		else {
			echo "</li>";
		}
	}
	echo "</ul>";
}

// Custom HTML menu
function getchtmlxmlmenu2($xml,$divlabel) {
	
		$html_li = function ($tag,$node) {
			
			$name = $node->attributes()["name"];
			
			if (isset($node->link) == TRUE) {
				$link = (string)$node->link;			
				echo "<a href=\"".$link."\">".$name."</a>";
			}
			else {
				echo $name;
			}
		};

	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
  	echo "<div>";
   //echo "<p class=\"divlabel\">".$divlabel."</p>";
   
	_menu_iter($html_li,$utilsxml,0);

	echo "</div>";
}
		


?>