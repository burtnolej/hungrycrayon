<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="stylesheets.js"></script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("dropdowns.xml");
	
	getxmlhtmlcselect($xml,$_GET,'label','dsearch');		
	
	$func = function() {
		global $SSDB;
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],NULL,"comment");
	};
	gethtmldiv("select filters",$func,"contain","divlabel");	
?>


<script src="dpivot.js"></script>
<script src="stylesheets.js"></script>
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script>

<?php

$_GET['parser']="drawform";

if(isset($_GET['ztypes'])) {
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

?>