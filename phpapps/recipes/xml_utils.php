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
			
		$results = ($item->xpath("parent::*"));
		
		if (sizeof($results) > 1) {
			throw new Exception("more than 1 match found");
		}
				
		return($results[0]);
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
	
	function get_child_details($item,$attrs,$parent_attrs) {
		$item = $this->__clean_args($item);
				
		$child_nodes=array();
		
		// extract children from the item 
		$children = $item->{$this->xpath_node};
				
		// iterate over each child
		foreach ($children as $child) {

			$child_nodes[] = $this->get_menuitem_details((string)$child->{$this->xpath_node_id},
									$attrs,$parent_attrs);
			
		}
		return($child_nodes);
	}
	
	
	need to add an optional arg here to provide tag to put in 
	results if $xpath_node_id not wanted	
	
	need to take out other references to a specific schema
	
	need to provide functions that return whole node rather than
	specific fields in nodes
	
	
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

		$results = ($this->xpath($xpath_str));
		
		if (sizeof($results) > 1) {
			throw new Exception("more than 1 match found");
		}
	
		return($results[0]);
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