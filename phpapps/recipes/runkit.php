<?php

//*
after the decorator is created the following functions exist

function powerup($base,$exp){
	// note the nested array as we are actually execing call_user_func_array twice
	return call_user_func_array('timer',array('timer_powerup',array($base,$exp));
}

function timer_powerup($base,$exp){
	printf("%d**%d=%d",$base,$exp,pow($base,$exp));
}

function timer($orig_func,$orig_func_args){
	$now = microtime(true);
	$orig_func_results = call_user_func_array($orig_func,$orig_func_args);
	$combined_results = sprintf("time:%s results:%s",$now,$orig_func_results);  
	echo $combined_results;
	return($orig_func_results);
}

*//

function decorator($orig_func,$decorator_func) {
	// rename the orig_func to something new
	$new_func = $decorator_func."_".$orig_func;
	runkit_function_rename($orig_func,$new_func);
	
	// create a new func (with orig_func name) that allows us 
	// to call the orig_func by its new name but actually executes 
	// the decorator_func with the orig_func parameters.
	// the decorator then calls the decoarator code followed by the
	// orig code
	$new_func_code = sprintf("return call_user_func_array('%s',array_merge(['%s'],[func_get_args()]));",$decorator_func, $new_func);			
	runkit_function_add($orig_func, '', $new_func_code);
}

function powerup($base,$exp){
	// func to decorate
	printf("%d**%d=%d",$base,$exp,pow($base,$exp));
}
	
function timer($orig_func,$orig_func_args){
	// decorator definition
	
	// code to decorate with
	$now = microtime(true);

	// run original function	
	$orig_func_results = call_user_func_array($orig_func,$orig_func_args);
	
	// combined output
	$combined_results = sprintf("time:%s results:%s",$now,$orig_func_results);  
	
	echo $combined_results;
	
	return($orig_func_results);
}

decorator('powerup', 'timer');

powerup(10,6);
?>