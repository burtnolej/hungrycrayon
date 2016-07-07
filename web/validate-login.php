
<html>
<style>

#menu {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 2em;
}
</style>
</html>

<?php

include "login.php";

function draw_menu($un,$pw) {

	if (($un=='guest') and ($pw=='welcome')) {
		echo "<div><center><br><br><br>";
                echo "<a id=menu href='business-plan.php'>The Business Plan</a><br>";
		echo "<a id=menu href='quad-visit.php'>Potential Projects for The Quad</a>";
		echo "</center></div>";
	}
	else {
		draw_login();
	}
}

if (!isset($_POST['username'])) {
	$un="guest";
}
else {
	$un=$_POST['username'];
}

if (!isset($_POST['password'])) {
	$pw="welcome";
}
else {
	$pw=$_POST['password'];
}

draw_menu($un,$pw);

?>
