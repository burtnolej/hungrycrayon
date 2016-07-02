<?php

abstract class StackTraceLevel {
    const AllFrames = -100;
    const LastFrame = 100;
}

$STACKTRACELEVEL = Null;

function __print_frame($frame,$frame_no) {	
	// clean up the frame for output
	printf("frame:%d function:%s\n",$frame_no,$frame["function"]);
	printf("frame:%d args:%s\n",$frame_no,implode(",",$frame["args"]));	
}	
	
function get_args_inscope($stacktrace,$frame_no=-1){

	
	switch($frame_no) {
		case StackTraceLevel::AllFrames: // print whole stack
			$frame_no=0;
			foreach ($stacktrace as $frame) {
				__print_frame($frame,$frame_no);
				$frame_no+=1	;
			}
			return;
			
		case StackTraceLevel::LastFrame: // print last frame
			$frame_no = sizeof($stacktrace) - 1;
			break;
	}
			
	// print specific frame 
	__print_frame($stacktrace[$frame_no],$frame_no);
}

function deeperdummyfunc($arg1,$arg2){
	
	global $STACKTRACELEVEL;
	
	// built in command to dump the current stack
	$st = debug_backtrace();

	// call user defn func to pull out relevant info from trace
	get_args_inscope($st,$STACKTRACELEVEL);
}

function dummyfunc($arg1,$arg2){
	deeperdummyfunc($arg1,$arg2);
}

// last frame
// expected results
// frame:1 function:dummyfunc
// frame:1 args:123,foobar
$GLOBALS['STACKTRACELEVEL'] = StackTraceLevel::LastFrame;
dummyfunc(123,"foobar");

// all frames
// expected results
// frame:0 function:deeperdummyfunc
// frame:0 args:123,foobar
// frame:1 function:dummyfunc
// frame:1 args:123,foobar
$GLOBALS['STACKTRACELEVEL'] = StackTraceLevel::AllFrames;
dummyfunc(123,"foobar");

// specific frame
// expected results
// frame:0 function:deeperdummyfunc
// frame:0 args:123,foobar
$GLOBALS['STACKTRACELEVEL'] = 0;
dummyfunc(123,"foobar");

