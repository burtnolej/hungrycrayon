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

function get_menuitem_html($menuid,$xml,$mi_depth=null) {
	
	// get node children
	
	$mi_details = get_menuitem_details($xml,$menuid,
							array('tag','label'),array('source'),
							'item','tag');
	
	if (!isset($mi_depth)) {
		$mi_depth = get_menuitem_depth($xml,$menuid,
								'label','root',
								'item','tag');
	}

	$html = sprintf("<li><a href='%s?arg=%s'>%s</a></li>",					
							$mi_details['source'],
							$mi_details['tag'],
							$mi_details['label']);	
							
	return($html);
}

$xml = new SimpleXMLElement($xmlstr);

print(get_menuitem_html("'configurephp'",$xml));

$item = get_menuitem($xml,"'configurephp'",
							'item','tag');

get_child_nodes($item,$xml);
?>
