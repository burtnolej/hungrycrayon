<?php

abstract class run_switch
{
    const alltests = "--all-tests";
    const testname = "--test-name";
    const listtests = "--list-tests";
    const usage = "--usage";
}

function __echoif($array,$key){
	if (array_key_exists($key,$array)) {
		echo $array[$key];
	}
}
	
function is_printable($element) {
	if (in_array(gettype($element),array('integer','string')) == true) {
		return true;
	}
	return false;
}

function boolstr($bool_val) {
	return($bool_val ? 'true' : 'false');
}

function get_stdobject(array $vars) {
	$_object = new StdClass();
	foreach ($vars as $key=>$val) {
		$_object->{$key} = $val;
	}
	return($_object);
}

function compareFiles($file_a, $file_b)
{
    if (filesize($file_a) == filesize($file_b))
    {
        $fp_a = fopen($file_a, 'rb');
        $fp_b = fopen($file_b, 'rb');

        while (($b = fread($fp_a, 4096)) !== false)
        {
            $b_b = fread($fp_b, 4096);
            if ($b !== $b_b)
            {
                fclose($fp_a);
                fclose($fp_b);
                return false;
            }
        }

        fclose($fp_a);
        fclose($fp_b);

        return true;
    }

    return false;
}

function get_file_lastline($file)
{
		$file = escapeshellarg($file); // for the security concious (should be everyone!)
		$line = `tail -n 1 $file`;
		
		return($line);
}

function nullfile($file)
{
	`cat /dev/null > application.log`;
}