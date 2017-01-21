
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
function getchtmlselect($column,$values,$widgetcount,$default,$args) {
	      
	if (isset($args['comment'])) {
		$comment=$args['comment'];
	}
	else {
		$comment=NULL;
	}
	
	if (isset($args['label'])) {
		$label=$args['label'];
	}
	else {
		$label=$column;
	}	
	
	echo "<p class=\"label\">".$label."</p>";
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
	
	/*if ($comment <> NULL) {
		echo "<p class=\"comment\">".$comment."</p>";
	}*/
	
	if ($comment <> NULL) {
		echo "<span class=\"comment\"><p>".$comment."</p></span>";
	}	
}

// Custom HTML Select - NO LABEL or COMMENT
function getchtmlselect_nolabel($column,$values,$widgetcount,$default,$comment) {

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
	echo "</span><br>";
}

// Custom HTML DB Select

function getchtmldbselect($dbname,$tablename,$column,$name,$widgetcount,$default,$args){
	
	if (isset($args['comment'])) {
		$comment=$args['comment'];
	}
	else {
		$comment=NULL;
	}
	
	if (isset($args['label'])) {
		$label=$args['label'];
	}
	else {
		$label=$column;
	}	
	
	if (isset($args['divlabel'])) {
		$divlabel=$args['divlabel'];
	}
	else {
		$divlabel=NULL;
	}	
	
	if ($divlabel<>NULL) {
		echo "<div class=\"contain\">";
		echo "<p class=\"divlabel\">".$divlabel."</p>";
	}
	
	if (isset($args['manualvalues'])) {
		$values =$args['manualvalues'];
	}
	else {
		if (isset($args['distinct'])) {
			if ($args['distinct'] == false) {
				$values = getfieldvalues($dbname,$column);	
			}
		}
		
		if (!isset($values)) {
			$values = getcolumndistinctvalues($dbname,$tablename,$column);
		}	
	}
		
	array_splice($values,0,0,"NotSelected");
	array_splice($values,1,0,"all");
	
	getchtmlselect($name,$values,$widgetcount,$default,$args);
	
	if ($divlabel<>NULL) {
		echo "</div>";
	}
}

// Custom HTML input
function getchtmlinput($label,$field,$default,$comment=NULL) {

	echo "<p class=\"label\">".$label."</p>";
	echo "<input class = \"custom\" type=\"text\" id=\"".$field."\" value=\"".$default."\" />";

	if ($comment <> NULL) {
		echo "<p class=\"comment\">".$comment."</p>";
	}
}

// Custom HTML XML input
function getxmlhtmlinput($xml,$defaults,$divlabel,$starttag=NULL) {
	
	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
	if ($starttag <> NULL) {		
		$tmproot = $utilsxml->xpath("//".$starttag);
		$_dropdowns = $tmproot[0]->xpath("./input");
	}
	else {
		$_dropdowns = $utilsxml->xpath("//input");
	}
	
	$widgetcount = 0;
	
	echo "<div class=\"contain\">";
	echo "<p class=\"divlabel\">".$divlabel."</p>";
		
	foreach ($_dropdowns as $_dropdown) {

		$field = (string)$_dropdown->field;
		$label = (string)$_dropdown->label;
		$default = NULL;

		if (array_key_exists($field,$defaults)) {
			$default = $defaults[$field];
		}
		elseif (isset($_dropdown->default)){
			$default = (string)$_dropdown->default;			
		}

		getchtmlinput($label,$field,$default,(string)$_dropdown->comment);
	}
	echo "</div>";
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

// Custom HTML XML Select
function getxmlhtmlcselect($xml,$defaults,$divlabel,$starttag=NULL) {
	      
	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
	if ($starttag <> NULL) {		
		$tmproot = $utilsxml->xpath("//".$starttag);
		$_dropdowns = $tmproot[0]->xpath("./select");
	}
	else {
	
		$_dropdowns = $utilsxml->xpath("//select");
	}
	
	$widgetcount = 0;
	
	echo "<div class=\"contain\">";
	echo "<p class=\"divlabel\">".$divlabel."</p>";
		
	foreach ($_dropdowns as $_dropdown) {
				
		$values = $_dropdown->values->xpath("child::value");
		$field = (string)$_dropdown->field;
		
		$args = array();
		
		if (isset($_dropdown->label)) {
			$args['label'] = (string)$_dropdown->label;
		}
		if (isset($_dropdown->comment)) {
			$args['comment'] = (string)$_dropdown->comment;
		}		
		$default = NULL;

		if (array_key_exists($field,$defaults)) {
			$default = $defaults[$field];
		}
		elseif (isset($_dropdown->default)){
			$default = (string)$_dropdown->default;			
		}

		getchtmlselect($field,$values,$widgetcount,$default,$args);
				
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
function getchtmlswitch($name,$value,$args) {

		if (isset($args['checked'])) {
			if (in_array($value,$args['checked'])) {
				$checked=TRUE;
			}
			else {
				$checked=FALSE;
			}
		}
		
		if (isset($args['comment'])) {
			$comment=$args['comment'];
		}
		else {
			$comment=NULL;
		}	
	
		echo "<p class=\"label switch\">".$name."</p>";
		echo "<label class=\"switch\">";
		
		echo "<input id=\"".$value."\" type=\"checkbox\" name=\"".$name."\"";

		if ($checked == TRUE) {
			echo "checked";
		}
		
		echo ">";
		echo "<div class=\"slider\"></div>";
		echo "</label>";

		if ($comment <> NULL) {
			echo "<span class=\"comment\"><p>".$comment."</p></span>";
	}	
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

function build_dbmenu_xml($dbname,$tablename,$colname) {
	
	$names = getcolumndistinctvalues($dbname,$tablename,$colname);

	 return build_menu_xml($names,"foobar","localhost","dpivot.php",array("yaxis"=>"adult"));
}

function build_menu_xml($keyarr,$menuname,$host="localhost",$script="dpivot.php",$args=NULL){
	
		$root=new SimpleXMLElement("<root></root>");
		$menuroot = $root->addChild("item");	
		$menuroot->addAttribute("name",$menuname);

		foreach ($keyarr as $label) {		
		
			$flags = array("xaxis"					=>"period",
											"yaxis"				=>"dow",
											"source_type"	=>"student", 
										 	"source"				=>"56newworkp",
											"source_value"=>$label,
											"cnstr_subject"=>"NotSelected",
											"cnstr_dow"		=>"NotSelected",
											"cnstr_period"	=>"NotSelected",
											"cnstr_student"=>"NotSelected",
											"cnstr_adult"	=>"NotSelected",
											"cnstr_prep"		=>"NotSelected",
											"formats"			=>"on",
											"rollup"				=>"on",
											"status"				=>"on",
											"student"			=>"on",
											"ztypes"				=>"subject,adult");
											
				if ($args <> NULL) {
					foreach ($args as $k=>$v) {
						$flags[$k] = $v;
					}
				}	
				
				$arr = array("ip"=>$host, "file"=>$script, "flags"=>$flags);
				
				$child = $menuroot->addChild("item");							
				$child->addAttribute("name",$label);
				$link = $child->addChild("link");
				assoc_array2xml($arr,$link);
		}
		
		return($root->asXML());
		//return($root);
}

function _get_menu_xml($root,$arr,$label) {

		$root->addAttribute("name",$label);
		$link = $child->addChild("link");
		assoc_array2xml($arr,$link);
}

function get_menu_xml($arr,$label) {
	
		$root=new SimpleXMLElement("<root></root>");
		$child = $root->addChild("item");
		$child->addAttribute("name",$label);
		$link = $child->addChild("link");
		assoc_array2xml($arr,$link);
		return($root->asXML());
}

// Custom HTML menu
function getchtmlxmlmenu2($xml,$divlabel) {

		$html_li = function ($tag,$node) {
			
			$name = $node->attributes()["name"];
			
			if (isset($node->link) == TRUE) {
				if (sizeof($node->link->children())>0) {
					$link = "http://".$node->link->ip."//".$node->link->file."?";
		
					$xpath_str = sprintf("./%s","flags");
					$items = $node->link->xpath($xpath_str);
		
					foreach ($items[0] as $key=>$value) {
						$link = $link.$key."=".$value."&";
					}
				}
				else {
					$link = (string)$node->link;			
				}
				echo "<a href=\"".$link."\">".$name."</a>";
			}
			else {
				echo $name;
			}
		};

	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
  	echo "<div id=\"wrap\">";
   //echo "<p class=\"divlabel\">".$divlabel."</p>";
   
	_menu_iter($html_li,$utilsxml,0);

	echo "</div>";
}

// 	div html
function gethtmldiv($label,$htmbodyfunc,$divclass=NULL,$pclass=NULL) {
	echo "<div ";
	if ($divclass<>NULL) { echo "class=\"".$divclass."\""; }
	echo ">";
	
	echo "<p ";
	if ($pclass<>NULL) { echo "class=\"".$pclass."\""; }
	echo ">".$label."</p> ";

	$htmbodyfunc();
	echo "</div>";
}


?>