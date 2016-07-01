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


#lvl1 {
    list-style:none;
    padding-left:0;
}
#lvl2 {
    list-style:none;
    padding-left:1em;
}
#lvl3 {
    list-style:none;
    padding-left:2em;
}
</style>
</html>

<?php

include 'xml_utils.php';
include 'menu.php';

function get_menuitem_html($xmlutils,$menuid,$mi_depth=null) {
	
	if (!isset($mi_depth)) {
		$mi_depth = $xmlutils->get_menuitem_depth($menuid);
	}
	
	$mi_children = $xmlutils->get_child_details($menuid,
					array('label','tag'),array('source'));

	$html="";
	
	foreach ($mi_children as $child) {
		$html = $html.sprintf("<li><a href='%s?arg=%s'>%s</a></li>",					
							$child['source'],
							$child['tag'],
							$child['label']).PHP_EOL;	
	}
				
	return($html);
}

$xmlutils = simplexml_load_string($xmlstr, 'XMLUtils');
$xmlutils->configure('label','root','item','tag');

print(get_menuitem_html($xmlutils,"buildingconfiguring"));

?>
