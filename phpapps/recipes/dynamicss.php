<?php


function setstylesheet($stylesheet) {
	echo '<link href="'.$stylesheet.'.css" rel="stylesheet" type="text/css" />';
}
?>

<!DOCTYPE html>
<html>
    <head>
    		<?php setstylesheet("common"); ?>
    </head>
    <body>
    	<p>foobar</p>
    </body>
<html>