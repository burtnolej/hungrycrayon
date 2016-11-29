<?php

/*

//$PHPLIBPATH = apache_getenv("PHPLIBPATH");


if (php_sapi_name() == 'cli') {
	echo "client";
	$PHPLIBPATH = getenv("PHPLIBPATH");
}
else {
	
	
	echo "server";
	foreach ($_ENV as $key => $val) {
		echo $key.'='.$val.PHP_EOL;
		echo "<br>";
	}
*/

$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);

include_once 'ui_utils.php';
include_once 'db_utils.php';

?>
