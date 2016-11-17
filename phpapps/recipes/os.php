
<?php

function isenvironset($env) {
	$libpath = getenv($env);
	
	if ($libpath == "") {
		return FALSE;
	}
	else {
		return $libpath;
	}
}

function prettyprint($msg,$value) {
	$str = str_pad($msg,30,"_",STR_PAD_LEFT);
	$str = $str." : ".$value;
	print $str.PHP_EOL;
}

function getenviron() {
	
	$api=php_sapi_name();
	
	prettyprint("script being interpretted by",$api);
	prettyprint("operating system",PHP_OS);

	$libpath = isenvironset('PHPLIBPATH');

	if  ($libpath== False) {
		print "error PHPLIBPATH not set";
	}
	else {
		prettyprint("PHPLIBPATH set to ",$libpath);
	}
	
	prettyprint("user name is",$_SERVER['LOGNAME']);
}

if (!debug_backtrace()) {
	getenviron();
}
?>