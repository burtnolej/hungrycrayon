<html>
<!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>-->
<script  type="text/javascript"  src="jquery-3.1.1.js"></script>
<script src="stylesheets.js"></script>
<script  type="text/javascript"  src="document_utils.js"></script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("inputs.xml");
	gethtmlbutton("button","submit");
	getxmlhtmlinput($xml,$_GET,'div label',"dedit");
	
?>

<script data-main="js/dedit.js" src="js/require.js"></script>
<script src="stylesheets.js"></script>
<script>

var Globals = <?php echo json_encode(array(
		'script_name' => $_SERVER['PHP_SELF'],
		'server_name' => $_SERVER['SERVER_NAME'],
 		'watch_list' => array("source_value"))); ?>;

</script>

<?php

if(isset($_GET['page_status'])) {
	echo "<br>update me<br>";
	$_GET['source_type']="update";
	//$_GET['source_value']="lesson";
	//$_GET['source_value']="id";
	$token =refreshpage();
	$_GET['parser']="drawform";
	
	//draw($token,$args);
}

if(isset($_GET['source_value'])) {
	$_GET['source_type']="id";
$_GET['parser']="drawform";
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

?>