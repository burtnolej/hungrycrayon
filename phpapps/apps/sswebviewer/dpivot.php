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
getxmlhtmlcselect($xml,$_GET,'this is a div label','dpivot');

$source_type = flip_source_type();
getchtmldbselect($SSDB,'lesson',$source_type,"source_value",1,$_GET['source_value'],'this is a div label','this is a comment');

$func = function() { getchtmlswitch("formats","formats",explode(",",$_GET['ztypes'])); };
gethtmldiv("select foo datatypes",$func,"contain","divlabel");

$func = function() {
	getchtmlswitch("status","status",explode(",",$_GET['ztypes']));
	getchtmlswitch("subject","subject",explode(",",$_GET['ztypes']));
	getchtmlswitch("adult","adult",explode(",",$_GET['ztypes']));
	getchtmlswitch("student","student",explode(",",$_GET['ztypes']));
};
gethtmldiv("select cell datatypes",$func,"contain","divlabel");		

$func = function() {
	global $SSDB;
	getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],NULL,"comment");				
	getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],NULL,"comment");				
	getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],NULL,"comment");				
	getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],NULL,"comment");
	getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],NULL,"comment");
};
gethtmldiv("select filters",$func,"contain","divlabel");	?>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="dpivot.js"></script>
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],
'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script></html>

<?php
if(isset($_GET['ztypes'])) {
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}
?>