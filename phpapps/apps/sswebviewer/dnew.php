<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="stylesheets.js"></script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("inputs.xml");
	
	create a dropdown to pick what type of lesson to create
	
	getxmlhtmlinput($xml,$_GET,'div label',"dedit");
	
?>

<script src="dpivot.js"></script>
<script src="stylesheets.js"></script>
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script>

<?php

$_GET['source_type']="id";
$_GET['parser']="drawform";

if(isset($_GET['source_value'])) {
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

?>