<html>
<style>

#nav {
    padding:10px;
    line-height:30px;
    background-color:#eeeeee;
    height:2000px;
    float:left;
    text-align:left;
    width: 200px;
    border: 3px solid #73AD21;
    <!margin: auto;>   
}

#lvl0 {
    list-style:none;
    padding-left:0;
}
#lvl1 {
    list-style:none;
    padding-left:1em;
}
#lvl2 {
    list-style:none;
    padding-left:2em;
}
#lvl3 {
    list-style:none;
    padding-left:3em;
}
</style>
</html>

<?php

include 'xml_utils.php';
include 'menu.php';


function get_menu_html($xmlutils,$item) {
	
	$item = $xmlutils->get_item($item);
	
	$html = sprintf("<li><a href='%s?arg=%s'>%s</a></li>",	
					$item->{'source'},
					$item->{'tag'},
					$item->{'label'}).PHP_EOL;					
					
	return($html);
}

function get_menu_level_html($xmlutils,$items,$item_depth){

	$html="<ul id='ul".$item_depth."'>".PHP_EOL;
			      
	foreach ($items as $_item) {
		$html = $html.sprintf("<li><a href='%s?arg=%s'>%s</a></li>",					
							$_item['source'],
							$_item['tag'],
							$_item['label']).PHP_EOL;
	}
	
	$html=$html."</ul>".PHP_EOL;
	
	return($html);
}
function get_menu_all_above_html($xmlutils,$menuid,$mi_depth=null) {
	
	if (!isset($mi_depth)) {
		$mi_depth = $xmlutils->get_item_depth($menuid);
	}
	
	$ancestor_details = $xmlutils->get_ancestor_details($menuid,
						array('label','tag'),array('source'));

	return(get_menu_level_html($xmlutils,$ancestor_details,$mi_depth));	
}

function get_menu_next_level_down_html($xmlutils,$menuid,$mi_depth=null) {
	
	if (!isset($mi_depth)) {
		$mi_depth = $xmlutils->get_item_depth($menuid);
	}
	
	$child_details = $xmlutils->get_children_details($menuid,
							array('label','tag'),array('source'));

	return(get_menu_level_html($xmlutils,$child_details,$mi_depth));		
}

$xmlutils = simplexml_load_string($xmlstr, 'XMLUtils');
$xmlutils->configure('tag','root','item','tag');

set_error_handler('\\XMLUtils::my_error_handler');

try {
	print(get_menu_all_above_html($xmlutils,"buildingconfiguring"));
	print(get_menu_html($xmlutils,"buildingconfiguring"));
	print(get_menu_next_level_down_html($xmlutils,"buildingconfiguring"));
} catch (Exception $e) {
	exception_handler($e);
}

?>
