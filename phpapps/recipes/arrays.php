
<?php
class recipe_arrays
{
    public function dump_array($array)
    {
        foreach ($array as $key => $value) {
            echo $key, $value;
        }
    }
}

function create_empty_array(){
	return array();
}

function append_to_array(&$array,$append_item){
	$array[] = $append_item;
}

/* basic array */
$basic_array = array(
    123,456
);

print_r($basic_array);
append_to_array($basic_array,789);
print_r($basic_array);

echo gettype(create_empty_array());

if (is_array(create_empty_array())){
	echo "its an array"; 
}
$array = array(
    "foo" => "bar",
    "bar" => "foo",
);
/* basic associative */



print join($array,",");


// array comprehension

$out=array_map(function($x) {return $x*$x;}, range(0, 9))

// array operators


if (array("foo","bar") == array("foo","bar")){
}
?>

	
	setattr
	getattr
	
	$array=array();
	foreach ($attrs as $attr) {
		$array[$attr] = $menu_item[$attr];
	}
	
	
	
for ($i = 1; $i <= 10; $i++) {
    echo $i;
}


if (in_array($b,array(1,2,3,4)) == true) { echo "true"; }


hp > $a = array(1,2,3,4,5,6);
php > 
php > 
php > array_shift($a);
php > print_r($a);
Array
(
    [0] => 2
    [1] => 3
    [2] => 4
    [3] => 5
    [4] => 6
)
php > $a = array(1,2,3,4,5,6);
php > $a1 = array_shift($a);
php > print_r($a1);
1

