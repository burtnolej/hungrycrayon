<?php

class XMLUtils extends SimpleXMLElement {

	function configure($root_tag, $root_tag_val,
								$xpath_node,$path_node_id) {
		
		// the unique tag and tag value that the root node will have
		// i.e. <label>root</label>
		$this->root_tag = $root_tag;
		$this->root_tag_val = $root_tag_val;
		
		// the tag name for the core tree node and the id tag that uniquely identifys it
		// i.e. <item><tag>foobar</tag></item>
		$this->xpath_node = $xpath_node;
		$this->xpath_node_id = $path_node_id;	
	}
	
	function __clean_args($item) {
		
		if (gettype($item) == 'object') {
			if (get_class($item) != 'XMLUtils') {
				//error
			}
			else {
				return($item);
			}
		}
		else {
			return($this->get_menuitem($item));
		}
	}
	
	function get_parent($item) {
		
		$item = $this->__clean_args($item);
					
		return($item->xpath("parent::*")[0]);
	}
	
	function get_ancestors($item) {
		
		$item = $this->__clean_args($item);
		
		$ancestors=array();
		while ($item->{$this->root_tag} != $this->root_tag_val) {
			$item= $this->get_parent($item);
			$ancestors[]=(string)$item->label;
		}
		return($ancestors);
	}
	
	function get_child_details($item) {
		$item = $this->__clean_args($item);
				
		$child_nodes=array();
		foreach ($item->{$this->xpath_node} as $child) {
			$child_nodes[] = $this->get_menuitem_details($child->tag,
									array('tag'),array('source'));
			
		}
		return($child_nodes);
	}
	
	function get_siblings($item) {
		
		$item = $this->__clean_args($item);
	
		$p_item = $this->get_parent($item);
		$siblings=array();
	
		
		foreach ($p_item->{$this->xpath_node} as $item) {
			$siblings[]=(string)$item->label;
		}
		return($siblings);
	}
	
	function get_menuitem($menuitemid) {
		
		if (is_string($menuitemid)) {
			$menuitemid = sprintf("'%s'",$menuitemid);
		}
		
		$xpath_str = sprintf("//%s[%s=%s]",
					$this->xpath_node,
					$this->xpath_node_id,
					$menuitemid);

		$menu_item = $this->xpath($xpath_str)[0];
	
		return($menu_item);
	}
	
	function get_menuitem_depth($menuitemid) {
		$item = $this->get_menuitem($menuitemid);
	
		$depth=0;
		while ($item->{$this->root_tag} != $this->root_tag_val) {
			$item= $this->get_parent($item);
			$depth++;
		}
		return($depth);
	}
	
	function get_menuitem_details($menuitemid,$attrs,$parent_attrs) {
	
		$menu_item = $this->get_menuitem($menuitemid);
		
		$parent_menu_item = $this->get_parent($menu_item);
		
		$array=array();
		foreach ($attrs as $attr) {
			
			$array[$attr] = (string)$menu_item->$attr;
		}
		
		foreach ($parent_attrs as $attr) {
			$array[$attr] = (string)$parent_menu_item->$attr;
		}	
		return($array);	
		
	}
}
?>