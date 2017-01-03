<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="stylesheets.js"></script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("dropdowns.xml");
	 gethtmlbutton("button","submit");
	getxmlhtmlcselect($xml,$_GET,'label','dnew')
	
?>

<script src="dnew.js"></script>
<script src="stylesheets.js"></script>
<script>var Globals = <?php echo json_encode(array(
  'script_name' => $_SERVER['PHP_SELF'],
  'server_name' => $_SERVER['SERVER_NAME'],
  'watch_list' => array("source_value")
  )); 
?>;</script>

<?php

if(isset($_GET['page_status'])) {
	$_GET['source_type']="add";
	$token =refreshpage();
	//$_GET['parser']="drawform";
	echo "<br><br>";
	draw($token,$args);
}
elseif(isset($_GET['source_value'])) {
	$_GET['source_type']="new";
	//$_GET['parser']="drawform";
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

/*
if(isset($_GET['page_status'])) {
	$_GET['source_type']="add";
	$token =refreshpage();
	$_GET['parser']="drawform";
	echo "<br><br>";
	draw($token,$args);
}
elseif(isset($_GET['source_value'])) {
	$_GET['source_type']="new";
	$_GET['parser']="drawform";
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}
*/

?>