
<html>
<style>
#menu {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 2em;
}
</style>
</html>

<?php

//include "sswebviewer-login.php";

if (!isset($_POST['xaxis'])) {
	echo "need to set xaxis";
}
else {
	$xaxis=$_POST['xaxis'];
}

if (!isset($_POST['yaxis'])) {
	echo "need to set yaxis";
}
else {
	$yaxis=$_POST['yaxis'];
}

echo "fetching table".$xaxis.",".$yaxis;

?>
