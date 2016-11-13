
<?php

$assoc_array = array(
    "foo" => "bar",
    "bar" => "foo"
);
    
foreach ($assoc_array as $key => $value)
{
    print($value);
}

$array = array(1,2,3,4,5,6,7);
for ($i=0;$i<=sizeof($array);$i++) {
	print($array[$i]).PHP_EOL;
	
}
/*

Arrayphp > 
php > 
php > $a=array("a"=>123, "b"=>456);
php > echo implode(",", $a);
123,456php > 


var_dump($a["a"]);

$i=1;
while ($i < 10) { echo $i++;}
*/

?>
