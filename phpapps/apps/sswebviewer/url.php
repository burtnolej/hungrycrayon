
<?php

function pop(&$array,$key) {
	$value = $array[$key];
	unset($array[$key]);
	return $value;
}

function buildurl($rooturl,$args,$viewer=False) {

	// only the viewer pages/service calls rely on get HTML GET args source_type/value to build the url
	if ($viewer==False) {
		
		// add last where source_type and source_value are not known server to replacea last with what was pivoted or listed last
		if (!isset($args['source_type'])) {
			$url = $rooturl."last/";
		}
		else {
				$url = $rooturl.$args['source_type']."/";
		}
		if (!isset($args['source_value'])) {
			$url = $url."last?";
		}
		else {
			$url = $url.$args['source_value']."?";
		}
	}
	
	foreach ($args as $key => $value){
		if ($value <> "") {
			if (is_array($value)) {
				$url = $url.$key."=".implode(",",$value)."&";
			}
			else {
				$url = $url.$key."=".$value."&";
			}
		}
	
		if ($value == "All") {
			$url = $url.$key."=&";
		}
	}
	return $url;
}

function getcurl($url) {
	
	$curl = curl_init($url);

	curl_setopt($curl, CURLOPT_VERBOSE,1);
	curl_setopt($curl, CURLOPT_RETURNTRANSFER,true);
	curl_setopt($curl, CURLOPT_HTTPHEADER, array("User-Agent: Test"));
	curl_setopt($curl, CURLOPT_HEADER,false);

	$token = curl_exec($curl);
	$http_status = curl_getinfo($curl, CURLINFO_HTTP_CODE);
	$stats = curl_getinfo($curl);
	curl_close($curl);
	
	return $token;
}
?>