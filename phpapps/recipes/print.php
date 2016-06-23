<?php


	print("$errno, $errstr, $errfile, $errline\n");
	
	
class print_recipe
{
    function padding()
    {
        echo sprintf("%'.9d\n", 123);
        echo sprintf("%'.09d\n", 123);
    }
}
?>