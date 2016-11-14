

<?php


function pop(&$array,$key) {
	$value = $array[$key];
	unset($array[$key]);
	return $value;
}

$array = array(
    "foo" => "bar",
    "bar" => "foo",
);

//$todelete = array_search('foo', $array);
//unset($array['foo']);
pop($array,'foo');
print_r($array);
?>