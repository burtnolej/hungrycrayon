<?php

include_once 'xml2html2.php';
include_once 'url.php';

$args = $_POST;
if (sizeof(array_keys($_POST)) == 0){
	$args = $_GET;
}

$url = buildurl('http://blackbear:8080/',$args);
$token = getcurl($url);
drawgrid($token,$args);

?>