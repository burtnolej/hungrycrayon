<?php

function get_power_str($base,$exp) {
	return(sprintf("\n%d**%d=%d\n",$base,$exp,pow($base,$exp)));

}

// POSITIVE TEST
$r1= get_power_str(12,4);

$r2 = call_user_func("get_power_str",12,4);

if ($r1 != $r2) {
	echo "FAILED";
} else { 
	echo "PASSED";
}

// NEGATIVE TEST

$r1= get_power_str(12,5);

$r2 = call_user_func("get_power_str",12,4);

if ($r1 == $r2) {
	echo "FAILED";
} else { 
	echo "PASSED";
}
?>