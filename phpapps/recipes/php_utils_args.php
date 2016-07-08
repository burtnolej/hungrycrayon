
<?php

$valid_switch_args = array('--usage');
$valid_key_val_args = array();
$valid_key_list_args = array();

class arg_handler {
	public function get_switch_arg((array) $valid_switch_args) {
	}
	public function get_key_val_arg((array) $valid_keyval_args) {
	}
	public function get_key_list_arg((array) $valid_keyval_args) {
	}
	
	public function check_arg(array $myargv = null) {
	
	// func    : take a list of arguments
	//
	// args    : $p_itemid - the unique id for the item
	//		     : $attrs - tags to extract from item
	//		     : $parent_attrs - tags to extract from parent
	//
	// returns : array of arrays 
	//		     : i.e. array[0] => array('attr1' => 'attr1val',
	//			  : 								'pattr1' => 'pattr1val')
			
	// if own arg array not passed in then use system detected args
	if (!isset($myargv)) {
		$myargv = array_shift($argv); // take off first param containing filename
	}
	
	for ($i=1;$i<sizeof($myargv);$i++) {
		
		// special case - if --usage passed in then display uage info and stop
		if ($myargv[$i] == run_switch::usage) {
			__usage();
			exit('exiting');
		}
	
		// single directive no value
		if ($myargv[$i] == run_switch::listtests) {
			$args[run_switch::listtests] = true;
			continue;
		}

		// names of specific tests to run
		if ($myargv[$i] == run_switch::testname) {
			
			while (!substr($myargv[$i],2) == '--') {
				echo $myargv[$i];
				$i++;
			}
			continue;
		}

		// directive with value - i.e. --test-name = <test-name>
		// so skip the next element inargv array
		$args[$myargv[$i]] = $myargv[$i+1];
		$i++;
	}
	
	return($myargv);
	
}
//if (sizeof($argv) == 1) {
//	__usage();
//	exit;
//}




