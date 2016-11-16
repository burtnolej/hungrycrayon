<?php

include_once 'xml2html2.php';
include_once 'url.php';

$args = $_POST;
if (sizeof(array_keys($_POST)) == 0){
	$args = $_GET;
}

//$funcname='drawgrid';

//if (isset($args['parser'])) {
//	$funcname=$args['parser'];
//}

$url = buildurl('http://blackbear:8080/',$args);
$token = getcurl($url);

draw($token,$args);
//call_user_func($funcname,$token,$args);

?>