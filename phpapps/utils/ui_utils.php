
<?php

set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
include_once 'db_utils.php';
include_once 'utils_xml.php';

function gethtmldropdown($column,$values,$widgetcount,$default=NULL) {

	$datalistname = "suggestions".$widgetcount;

	echo "<label for=\"".$column."\" >".$column."</label>";
	//echo "<input type=\"text\" name=\"".$column."\" id=\"".$column."\" list=\"".$datalistname."\" autocomplete=\"off\" ";
	echo "<input type=\"text\" name=\"".$column."\" id=\"".$column."\" list=\"".$datalistname."\""; 

	if ($default <> NULL) {
		echo " value=\"".$default."\"";
	}	
	
	echo ">";
	echo "<datalist id=\"".$datalistname."\">";
	
	foreach ($values as $value) {
			echo "<option>".$value."</option>";
		}
		
	echo "</datalist>";
}

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

function gethtmltablecoldropdown($dbname,$tablename,$column,$widgetcount,$default=NULL){
	
	echo "<div class=\"container\">";
		
	$values = getcolumndistinctvalues($dbname,$tablename,$column);

	gethtmldropdown($column,$values,$widgetcount,$default);
	
	$widgetcount = $widgetcount+1;
	
	echo "</div>";

}

function gethtmlxmldropdown($xml) {
	
	$utilsxml = simplexml_load_string($xml,'utils_xml');
	
	$_dropdowns = $utilsxml->xpath("//dropdown");
	
	$widgetcount = 0;
	
	foreach ($_dropdowns as $_dropdown) {
			
		echo "<div class=\"container\">";

		$values = $_dropdown->values->xpath("child::value");

		gethtmldropdown($_dropdown->field,$values,$widgetcount);
	
		$widgetcount = $widgetcount+1;
	
		echo "</div>";
	}
}

function gethtmlbutton($type,$label) {
	
	echo "<input type=\"".$type."\" name=\"".$type."\" value=\"".$label."\" />";

}

function gethtmlmultiselect($dbname,$query,$name) {
	
		//echo "<div class=\"container\">";
		//echo "<div style=\"width: 12em; float: bottom;\">";
		
		$db = new SQLite3($dbname);

		$results = $db->query($query);
		while ($row = $results->fetchArray()) {
				echo "<input id=\"".$row['name']."\" type=\"checkbox\" name=\"".$name."[]\" value=\"".$row['name']."\"/>";
				echo "<label for=\"".$row['name']."\" >".$row['name']."</label>";
				echo "<br>";
		}
		//echo "</datalist>";
		//echo "</div></div>";
}
?>