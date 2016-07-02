<?php

/*
	get_child_details($item,$attrs,$parent_attrs)
	get_menuitem($menuitemid)
	get_menuitem_depth($menuitemid)
	get_menuitem_details($menuitemid,$attrs,$parent_attrs)

	get_siblings($item,$tag=null)	
	get_children($item)
	get_parent($item)
	get_ancestors($item)
	get_item
	get_item_details
	get_details
*/
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
			return($this->get_item($item));
		}
	}
	
	function __check_args($item,$attrs,$parent_attrs) {
		if (!$this->__is_SimpleXMLElement($item) == true) {
			throw new Exception(sprintf("1st parameter must implement SimpleXMLElement: got %s",gettype($item)));
		}

		if ((!is_array($attrs)) or (!is_array($parent_attrs))) {
			throw new Exception("Paramter 2 & 3 must be arrays");
		}
		return true;
	}
	
	function __is_SimpleXMLElement($item) {
	
		if (!gettype($item) == 'object') {
			return false;
		}
		
		if ((!method_exists($item,'xpath') == true) or 
				(!method_exists($item,'registerXPathNamespace') == true)) {
					return false;					
		}
		return true;
	}
	
	// ------------------------------------------------------------------
	// get details for specific groups of family members ----------------
	// ------------------------------------------------------------------

	function get_children_details($p_item,$attrs,$parent_attrs) {
	

		if (gettype($p_item) != 'integer') {
			throw new Exception(sprintf("1st parameter must be integer: got %s",
				gettype($p_item)));
		}
		    
		if (gettype($attrs) != 'array') {
			throw new Exception(sprintf("2nd parameter must be array: got %s",
				gettype($item)));
		}
		
		if (gettype($parent_attrs) != 'array') {
			throw new Exception(sprintf("3rd parameter must be array: got %s",
				gettype($item)));
		}
		          		
		$p_item = $this->__clean_args($p_item);
		
		$children = $this->get_children($p_item);
		
		$child_details = $this->get_details($children,$attrs,$parent_attrs);
													
		return($child_details);
	}
	
	function get_ancestor_details($item,$attrs,$parent_attrs) {
	
		if (gettype($item) != 'integer') {
			throw new Exception(sprintf("1st parameter must be integer: got %s",
				gettype($item)));
		}
		    
		if (gettype($attrs) != 'array') {
			throw new Exception(sprintf("2nd parameter must be array: got %s",
				gettype($item)));
		}
		
		if (gettype($parent_attrs) != 'array') {
			throw new Exception(sprintf("3rd parameter must be array: got %s",
				gettype($item)));
		}
		
		$item = $this->__clean_args($item);
		
		$ancestors = $this->get_ancestors($item);

		$ancestor_details = $this->get_details($ancestors,$attrs,$parent_attrs);
													
		return($ancestor_details);
	}
	
	function get_sibling_details($item,$attrs,$parent_attrs) {
	
		if (gettype($item) != 'integer') {
			throw new Exception(sprintf("1st parameter must be integer: got %s",
				gettype($item)));
		}
		    
		if (gettype($attrs) != 'array') {
			throw new Exception(sprintf("2nd parameter must be array: got %s",
				gettype($item)));
		}
		
		if (gettype($parent_attrs) != 'array') {
			throw new Exception(sprintf("3rd parameter must be array: got %s",
				gettype($item)));
		}
		
		// clean args
		$item = $this->__clean_args($item);
		
		$siblings = $this->get_siblings($item);
		
		$sibling_details = $this->get_details($siblings,$attrs,$parent_attrs);
													
		return($sibling_details);
	}
	
	// ------------------------------------------------------------------
	// get objects for specific groups of family members ----------------
	// ------------------------------------------------------------------

	function get_parent($item) {
		
		// check args
		if (!$this->__is_SimpleXMLElement($item) == true) {
			throw new Exception(sprintf("1st parameter must implement SimpleXMLElement: got %s",gettype($item)));
		}

		$item = $this->__clean_args($item);
			
		$results = ($item->xpath("parent::*"));
		
		if (sizeof($results) > 1) {
			throw new Exception("more than 1 match found");
		}
			
		return($results[0]);
	}

	
	function get_ancestors($item) {
		// check args
		if (!$this->__is_SimpleXMLElement($item) == true) {
			throw new Exception(sprintf("1st parameter must implement SimpleXMLElement: got %s",gettype($item)));
		}

		$ancestors=array();
		while ($item->{$this->root_tag} != $this->root_tag_val) {
			$item= $this->get_parent($item);
			$ancestors[]=$item;
		}
		return($ancestors);
	}
	
	function get_siblings($item) {
		
		// func    : by comparing the parent id of each subitem to the id of $item
		//         : gets all of the siblings. Does return itself in siblings.
		//
		// args    : $item - the unique id for the item or the item itself
		//         : as an object.
		//
		// returns : array of arrays 
		//		     : i.e. array[0] => array('attr1' => 'attr1val',
		//			  : 								'pattr1' => 'pattr1val')

		// check args
		if (!$this->__is_SimpleXMLElement($item) == true) {
			throw new Exception(sprintf("1st parameter must implement SimpleXMLElement: got %s",gettype($item)));
		}
	
		$p_item = $this->get_parent($item);
		
		$siblings = $this->get_children($p_item);

		return($siblings);
	}
	
	function get_children($p_item) {
		
		// func    : gets all of the children nodes of a particular item
		//
		// args    : $itemid - the unique id for the item or the item itself
		//         : as an object.
		//
		// returns : array of objects
		
		// check args
		if (!$this->__is_SimpleXMLElement($p_item) == true) {
			throw new Exception(sprintf("1st parameter must implement SimpleXMLElement: got %s",gettype($item)));
		}
		
		$children=array();
		
		$xpath_str = sprintf("//%s",$this->xpath_node);
		$items = $this->xpath($xpath_str);
		
		foreach ($items as $item) {
			$_parent = $this->get_parent($item);

			if ($_parent->{$this->xpath_node_id} == 
			  		$p_item->{$this->xpath_node_id}) {
			  			$children[] = $item;  
			}
		}
		
		return($children);
	}
	
	// ------------------------------------------------------------------
	// low level accessors-----------------------------------------------
	// ------------------------------------------------------------------
	function get_details($items,$attrs,$parent_attrs) {
		
		// func    : loops over array of items, retreiving the details
		//  	     : where details are the tags specified in $attrs/$parent_attrs
		//			  : a request for just 1 item is implemented as passing in an 
		//         : array of size 1
		//
		// args    : $items - array of objects
		//		     : $attrs - tags to extract from item
		//		     : $parent_attrs - tags to extract from parent
		//
		// returns : array of arrays 
		//		     : i.e. array[0] => array('attr1' => 'attr1val',
		//			  : 								'pattr1' => 'pattr1val')
		
		// check args
		

		if (gettype($items) != 'array') {
			throw new Exception(sprintf("1st parameter must be array: got %s",
				gettype($item)));
		}
		    
		if (gettype($attrs) != 'array') {
			throw new Exception(sprintf("2nd parameter must be array: got %s",
				gettype($item)));
		}
		
		if (gettype($parent_attrs) != 'array') {
			throw new Exception(sprintf("3rd parameter must be array: got %s",
				gettype($item)));
		}
		          		
		$items_detail=array();
				
		foreach ($items as $itemid=>$item) {

			$items_detail[] = $this->get_item_details($item,
												$attrs,$parent_attrs);										
		}

		return($items_detail);
	}
	
	function get_item_details($item,$attrs,$parent_attrs) {

		// func    : gets the detail for a particular item
		//  	     : where details are the tags specified in $attrs/$parent_attrs
		//
		// args    : $item - the item object 
		//		     : $attrs - tags to extract from item
		//		     : $parent_attrs - tags to extract from parent
		//
		// returns : array 
		//		     : i.e. array('attr1' => 'attr1val',
		//			  : 			   'pattr1' => 'pattr1val')

		$root=false;
		
		// check args
		$this->__check_args($item,$attrs,$parent_attrs);
		
		// is this the root node ?		
		if ($item->{$this->root_tag} == $this->root_tag_val) {
			$root=true;
		}
		
		if (!$root==true) {
			$parent_item = $this->get_parent($item);
		}
		
		$details=array();
		foreach ($attrs as $attr) {
			$details[$attr] = (string)$item->$attr;
		}
		
		if (!$root==true) {
			foreach ($parent_attrs as $attr) {
				$details[$attr] = (string)$parent_item->$attr;
			}
		}
		else {
			foreach ($parent_attrs as $attr) {
				$details[$attr] = "";
			}
		}
		
		return($details);		
	}

	function get_item($itemid) {
		
		// func    : gets the object for a particular item using the 
		//         : the unique id to search by
		//
		// args    : $itemid - the unique id for the item or the item itself
		//
		// returns : object 
		
		if (is_string($itemid)) {
			$itemid = sprintf("'%s'",$itemid);
		}
		
		$xpath_str = sprintf("//%s[%s=%s]",
					$this->xpath_node,
					$this->xpath_node_id,
					$itemid);
		
		$items = ($this->xpath($xpath_str));
		
		if (sizeof($items) > 1) {
			throw new Exception("more than 1 match found");
		}
	
		return($items[0]);
	}
	
	function get_item_depth($menuitemid) {
		$item = $this->get_item($menuitemid);
	
		$depth=0;
		while ($item->{$this->root_tag} != $this->root_tag_val) {
			$item= $this->get_parent($item);
			$depth++;
		}
		return($depth);
	}	
}
?>