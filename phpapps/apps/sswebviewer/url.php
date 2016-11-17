
<?php

function pop(&$array,$key) {
	$value = $array[$key];
	unset($array[$key]);
	return $value;
}

function buildurl($rooturl,$args,$viewer=False) {
	
	// only the viewer pages/service calls rely on get args source_type/value to build the url
	if ($viewer==False) {
		$url = $rooturl.$args['source_type']."/";
		$url = $url.$args['source_value']."?";
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