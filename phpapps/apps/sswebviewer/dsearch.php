<!DOCTYPE html>
<html>
<link rel="stylesheet" type="text/css" href="css/select.css" />
<link rel="stylesheet" type="text/css" href="css/div.css" />
<link rel="stylesheet" type="text/css" href="css/switch.css" />
<link rel="stylesheet" type="text/css" href="css/menu.css" />
</html>
<html>
			<?php 
			
				include_once 'bootstrap.php';
				
				initpage();
				
				$xml = file_get_contents("dropdowns.xml");
				
				echo "<div id=\"content\">";
				
				getxmlhtmlcselect($xml,$_GET,'label','dsearch');		
				
				echo "<div class=\"contain\">";
				echo "<p class=\"divlabel\">search criteria</p>";
				getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],NULL,"comment");
				echo "<br>";
				getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],NULL,"comment");
				echo "<br>";
				getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],NULL,"comment");
				echo "<br>";
				getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],NULL,"comment");
				echo "<br";
				getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],NULL,"comment");
				echo "</div>";
				echo "</div>";
				?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="dpivot.js"></script>
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],
'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script>

</html>

<?php

$_GET['parser']="drawform";

if(isset($_GET['ztypes'])) {
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

?>