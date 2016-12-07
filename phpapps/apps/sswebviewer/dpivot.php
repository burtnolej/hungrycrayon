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
				
				$xml = file_get_contents("dropdowns.xml");
				$menuxml =file_get_contents("menus.xml");
								
				getdbinfo();

				set_include_path($PHPLIBPATH);

				include_once 'ui_utils.php';
				include_once 'db_utils.php';
				include_once 'xml2html2.php';
				include_once 'url.php';
				
				getchtmlxmlmenu2($menuxml,"label");
				
				echo "<div id=\"content\">";
				
				getxmlhtmlcselect($xml,$_GET,'this is a div label','dpivot');

				set_stylesheet();
				
				$source_type = flip_source_type();
				
				getchtmldbselect($SSDB,'lesson',$source_type,"source_value",1,$_GET['source_value'],
				'this is a div label','this is a comment');

				echo "<div class=\"contain\">";
				echo "<p class=\"divlabel\">select cell datatypes</p>";
				getchtmlswitch("formats","formats",explode(",",$_GET['ztypes']));
				echo "</div>";

				echo "<div class=\"contain\">";
				echo "<p class=\"divlabel\">select cell datatypes</p>";
				getchtmlswitch("status","status",explode(",",$_GET['ztypes']));
				getchtmlswitch("subject","subject",explode(",",$_GET['ztypes']));
				echo "<br>";
				getchtmlswitch("adult","adult",explode(",",$_GET['ztypes']));
				getchtmlswitch("student","student",explode(",",$_GET['ztypes']));
				echo "</div>";		
				
				echo "<div class=\"contain\">";
				echo "<p class=\"divlabel\">select cell datatypes</p>";
				
				getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],NULL,"comment");				
				getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],NULL,"comment");				
				getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],NULL,"comment");				
				getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],NULL,"comment");
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

if(isset($_GET['ztypes'])) {

	$SSRESTURL = getenv("SSRESTURL");

	if ($SSRESTURL == "") {
		trigger_error("Fatal error: env SSRESTURL must be set", E_USER_ERROR);
	}

	$args = $_POST;
	if (sizeof(array_keys($_POST)) == 0){
		$args = $_GET;
	}

	if (isset($args['trantype']) == True) {
		switch ($args['trantype']) {
    		case 'new':
      		$url = buildurl($SSRESTURL.'new',$args);
      	break;
    		default:
				$url = buildurl($SSRESTURL,$args);
		}
	}
	else {
		$url = buildurl($SSRESTURL,$args);
	}

	$token = getcurl($url);
echo "<br><br>";


draw($token,$args);

}

?>