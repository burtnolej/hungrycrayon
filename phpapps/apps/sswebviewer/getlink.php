<?php

include_once 'xml2html2.php';
include_once 'url.php';

$args = $_POST;
if (sizeof(array_keys($_POST)) == 0){
	$args = $_GET;
}

if (isset($args['trantype']) == True) {
	switch ($args['trantype']) {
    case 'new':
      $url = buildurl('http://blackbear:8080/new',$args);
      break;
    default:
    	$url = buildurl('http://blackbear:8080/',$args);
	}
}
else {
	$url = buildurl('http://blackbear:8080/',$args);
}

$token = getcurl($url);
draw($token,$args);

?>