<?php

include_once 'xml2html2.php';
include_once 'url.php';

$SSRESTURL = getenv("SSRESTURL");

if ($SSRESTURL == "") {
	trigger_error("Fatal error: env SSRESTURL must be set", E_USER_ERROR);
}

$args = $_POST;
if (sizeof(array_keys($_POST)) == 0){
	$args = $_GET;
}

if (isset($args['trantype']) == True) {
	switch ($args['trantype']) {
    case 'new':
      //$url = buildurl('http://blackbear:8080/new',$args);
      $url = buildurl($SSRESTURL.'new',$args);
      break;
    default:
    	//$url = buildurl('http://blackbear:8080/',$args);
		$url = buildurl($SSRESTURL,$args);
	}
}
else {
	//$url = buildurl('http://blackbear:8080/',$args);
	$url = buildurl($SSRESTURL,$args);
}

$token = getcurl($url);
draw($token,$args);

?>