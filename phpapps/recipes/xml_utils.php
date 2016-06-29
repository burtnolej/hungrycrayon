<?php

function __clean_args($item, $tree) {
	
	if (gettype($item) == 'object') {
		if (get_class($item) != 'SimpleXMLElement') {
			//error
		}
		else {
			return($item);
		}
	}
	else {
		if ($tree != null) {
			return(get_menuitem($tree,$item));
		}
		else {
			// error
		}
	}
}

function get_parent($item,$tree=null) {
	
	$item = __clean_args($item,$tree);
		
	return($item->xpath("parent::*")[0]);
}

function get_ancestors($item,$root_tag,$tree=null) {
	
	$item = __clean_args($item,$tree);
	
	$ancestors=array();
	while ($item->label != $root_tag) {
		$item= get_parent($item);
		$ancestors[]=(string)$item->label;
	}
	return($ancestors);
}


function get_child_nodes($item,$tree=null) {
	$item = __clean_args($item,$tree);
	
	print_r($item);
	
	//$child_nodes=array();
	//foreach ($item->item as $child) {
	//		$child_nodes[] = $child;
	//}

	//return($child_nodes);
}


function get_siblings($item, $tree=null) {
	
	$item = __clean_args($item,$tree);

	$p_item = get_parent($item);
	$siblings=array();

	foreach ($p_item->menuitem as $item) {
		$siblings[]=(string)$item->label;
	}
	return($siblings);
}

function get_menuitem($tree,$menuitemid,$xpath_node=null,$xpath_node_id=null) {
	
	if (isset($xpath_node) and isset($xpath_node_id)) {
		
		$xpath_str = sprintf("//%s[%s=%s]",
					$xpath_node,
					$xpath_node_id,
					$menuitemid);
	}
	else {
		$xpath_str = sprintf("//menuitem[menuitemid=%s]",$menuitemid);
	}
	
	$menu_item = $tree->xpath($xpath_str)[0];

	return($menu_item);
	
}

function get_menuitem_depth($tree,$menuitemid,$root_node,$root_node_val,$xpath_node=null,$xpath_node_id=null) {
	$item = get_menuitem($tree,$menuitemid,$xpath_node,$xpath_node_id);

	$depth=0;
	while ($item->$root_node != $root_node_val) {
		$item= get_parent($item);
		$depth++;
	}
	return($depth);
}

function get_menuitem_details($tree,$menuitemid,$attrs,$parent_attrs,
					$xpath_node=null,$xpath_node_id=null) {

	$menu_item = get_menuitem($tree,$menuitemid,$xpath_node,$xpath_node_id);
	$parent_menu_item = get_parent($menu_item);
	
	$array=array();
	foreach ($attrs as $attr) {
		
		$array[$attr] = (string)$menu_item->$attr;
	}
	
	foreach ($parent_attrs as $attr) {
		$array[$attr] = (string)$parent_menu_item->$attr;
	}	
	return($array);	
	
}
?>