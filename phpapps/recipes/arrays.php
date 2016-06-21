
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

/* basic */
$array = array(
    "foo" => "bar",
    "bar" => "foo",
);

/* type casting */
?>

