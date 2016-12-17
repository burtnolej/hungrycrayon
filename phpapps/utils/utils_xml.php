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

//include 'utils.php';

class utils_xml extends SimpleXMLElement {

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
		
	function is_SimpleXMLElement($item) {
			
		if ((!method_exists($item,'xpath') == true) or 
				(!method_exists($item,'registerXPathNamespace') == true)) {
					return false;					
		}
		return true;
	}
	
	// ------------------------------------------------------------------
	// get details for specific groups of family members ----------------
	// ------------------------------------------------------------------

	function get_children_details($p_itemid,array $attrs, array $parent_attrs) {
	
		// func    : get details for all of the children of a given parent
		//
		// args    : $p_itemid - the unique id for the item
		//		     : $attrs - tags to extract from item
		//		     : $parent_attrs - tags to extract from parent
		//
		// returns : array of arrays 
		//		     : i.e. array[0] => array('attr1' => 'attr1val',
		//			  : 								'pattr1' => 'pattr1val')
		
		// cannot hint at non object type so test directly
		if (!in_array(gettype($p_itemid),array('integer','string')) == true) {
			throw new Exception(sprintf("1st parameter must be integer or string: got %s",
				gettype($p_itemid)));
		}
		    
		$p_item = $this->get_item($p_itemid);
		
		$children = $this->get_children($p_item);
		
		$child_details = $this->get_details($children,$attrs,$parent_attrs);
													
		return($child_details);
	}
	
	function get_ancestor_details($itemid,array $attrs,array $parent_attrs) {

		// func    : get details for all of the children of a given parent
		//
		// args    : $p_itemid - the unique id for the item
		//		     : $attrs - tags to extract from item
		//		     : $parent_attrs - tags to extract from parent
		//
		// returns : array of arrays 
		//		     : i.e. array[0] => array('attr1' => 'attr1val',
		//			  : 								'pattr1' => 'pattr1val')
	
		if (!in_array(gettype($itemid),array('integer','string')) == true) {
			throw new Exception(sprintf("1st parameter must be integer or string: got %s",
				gettype($itemid)));
		}
				
		$item = $this->get_item($itemid);
		
		$ancestors = $this->get_ancestors($item);

		$ancestor_details = $this->get_details($ancestors,$attrs,$parent_attrs);
													
		return($ancestor_details);
	}
	
	function get_sibling_details($itemid,array $attrs,array $parent_attrs) {
	
		// func    : get details for all of the children of a given parent
		//
		// args    : $p_itemid - the unique id for the item
		//		     : $attrs - tags to extract from item
		//		     : $parent_attrs - tags to extract from parent
		//
		// returns : array of arrays 
		//		     : i.e. array[0] => array('attr1' => 'attr1val',
		//			  : 								'pattr1' => 'pattr1val')
		
		if (!in_array(gettype($itemid),array('integer','string')) == true) {
			throw new Exception(sprintf("1st parameter must be integer or string: got %s",
				gettype($itemid)));
		}
		    
		$item = $this->get_item($itemid);
		
		$siblings = $this->get_siblings($item);
		
		$sibling_details = $this->get_details($siblings,$attrs,$parent_attrs);
													
		return($sibling_details);
	}
	
	// ------------------------------------------------------------------
	// get objects for specific groups of family members ----------------
	// ------------------------------------------------------------------

	function get_parent(SimpleXMLElement $item) {
		
		// func    : get the parent for a particular object
		//
		// args    : $item - object of class SimpleXMLElement
		//
		// returns : a SimpleXMLElement object
		
		$results = ($item->xpath("parent::*"));
		
		if (sizeof($results) > 1) {
			throw new Exception("more than 1 match found");
		}
			
		return($results[0]);
	}
	
	function get_ancestors(SimpleXMLElement $item) {

		// func    : get the ancestors for a particular object
		//
		// args    : $item - object of class SimpleXMLElement
		//
		// returns : an array of SimpleXMLElement object
		
		$ancestors=array();
		while ($item->{$this->root_tag} != $this->root_tag_val) {
			$item= $this->get_parent($item);
			$ancestors[]=$item;
		}
		return($ancestors);
	}
	
	function get_siblings(SimpleXMLElement $item) {
		
		// func    : gets the siblings for a particular object
		//
		// args    : $item - object of class SimpleXMLElement
		//
		// returns : array of arrays 
		//		     : i.e. array[0] => array('attr1' => 'attr1val',
		//			  : 								'pattr1' => 'pattr1val')

		$p_item = $this->get_parent($item);
		
		$siblings = $this->get_children($p_item);

		return($siblings);
	}
	
	function get_children(SimpleXMLElement $p_item) {
		
		// func    : gets all of the children nodes of a particular item
		//
		// args    : $itemid - the unique id for the item or the item itself
		//         : as an object.
		//
		// returns : array of SimpleXMLElement objects
		
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
	function get_details(array $items,array $attrs,array $parent_attrs) {
		
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
				
		$items_detail=array();
				
		foreach ($items as $itemid=>$item) {

			$items_detail[] = $this->get_item_details($item,
												$attrs,$parent_attrs);										
		}

		return($items_detail);
	}
	
	function get_item_details(SimpleXMLElement $item,array $attrs,array $parent_attrs) {

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

	function get_item($itemid,$node=NULL,$nodeid=NULL) {
		
		// func    : gets the object for a particular item using the 
		//         : the unique id to search by
		//
		// args    : $itemid - the unique id for the item or the item itself
		//
		// returns : object 
		
		if (is_string($itemid)) {
			$itemid = sprintf("'%s'",$itemid);
		}
		
		if ($node <> NULL and $nodeid <> NULL) {
			$xpath_str = sprintf("//%s[%s=%s]",$node,$nodeid,$itemid);
		}
		else {
			$xpath_str = sprintf("//%s[%s=%s]",
					$this->xpath_node,
					$this->xpath_node_id,
					$itemid);
		}
		
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
	
	function xml_iter($func,$root=NULL){
		if ($root==NULL) {
			$root=$this;
		}
			foreach ($root as $tag => $node) {
				$func($tag,$node);

				if (sizeof($node ->children()) <> 0) {
					$this-> xml_iter($func,$node);
				}
			}
	}
}

	function assoc_array2xml($arr,$root)  {
		foreach ($arr as $k=>$v) {
			
			if (is_array($v)) {
				$child = $root->addChild($k);
				assoc_array2xml($v,$child); 
			}
			else {
				$root->addChild($k,$v);
			}
		}
	}
	
	function append_xml($sourceroot,$targetroot) {
	
	foreach ($sourceroot as $tag=>$sourcenode) {
		if (sizeof($sourcenode ->children()) <> 0) {
			$targetnode = $targetroot->addchild($tag);
			foreach ($sourcenode->attributes() as $attr=>$attrvalue) {
				$targetnode[$attr] = (string)$attrvalue;
			}
			append_xml($sourcenode,$targetnode);
		}
		else {
			$targetnode = $targetroot->addchild($tag,$sourcenode);
		}
	}
}
		
?>