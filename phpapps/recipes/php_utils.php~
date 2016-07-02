<?php

function pprint_stack($basename,$funcname,$lineno,$args,$fulltrace,$padstr=" ") {	
	
	printf("%s|%s|%s|%s|%s\n",str_pad($basename,20,$padstr),
								str_pad($funcname,30,$padstr),
								str_pad($lineno,10,$padstr),
								str_pad($args,30,$padstr),"");
								//str_pad($fulltrace,150,$padstr));
}

function exception_handler($e) {

	echo PHP_EOL.'Exception: ',$e->getMessage(),"\n\n";
	$stack_as_array = split("\n",$e->getTraceAsString());
	$i=0;
	pprint_stack('basename','funcname','lineno','args','fulltrace');
	pprint_stack('','','','','','-');
	
	foreach ($stack_as_array as $frame) {
		
		// make sure full frame output line
		if (strpos($frame,':') !== false) {
			
				// split frame by colon into 3 vars
				list($fullpath, $rest) = explode(":",substr($frame,3));
				
				// find the start of the args in the non path section
				$open_bracket_posn = strpos($rest,'(');
					
				// put args into an array
				$args_str = substr($rest,$open_bracket_posn+1,-1);
				
				// get the func name 
				$func_name = substr($rest,1,$open_bracket_posn-1);
								
				// get the lineno
				$open_bracket_posn = strpos(basename($fullpath),'(');
				$lineno = substr(basename($fullpath),$open_bracket_posn+1,-1);
				
				// get the source file basename
				$basename = substr(basename($fullpath),0,$open_bracket_posn);
				
				pprint_stack($basename, $func_name, $lineno, $args_str,$frame);
		}
	}
	echo PHP_EOL;	
}
?>