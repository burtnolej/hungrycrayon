<!DOCTYPE html>
<html>
<link rel="stylesheet" type="text/css" href="custom-select.css" />
<link rel="stylesheet" type="text/css" href="default.css" />

<section>
    <div id="one"></div>
    <div id="two"></div>
    <div id="three"></div>
    <div id="four"></div>
    <div id="five"></div>
</section>

<style>
label {
	display: inline-block;
	width:120px;
	text-alight=right;
}

div#one {
    float: left;
}
div#two {
    float: left;
}
div#three {
    float: left;
}
div#four {
    float: left;
}
div#five {
    position: absolute;
    top :300px;
}

</style>

</html>
<html>
<div id="fsf">

			<?php 
			
					$xml = "<root>
									<select id='1'>
										<field>source_type</field>
										<values>
											<value>list</value>
										</values>
										<default>list</default>
									</select>
									<select id='2'>
										<field>source_value</field>
										<values>
											<value>lesson</value>
										</values>
										<default>lesson</default>
									</select>
									<select id='3'>
										<field>pagenum</field>
										<values>
											<value>1</value>
											<value>2</value>
										</values>
										<default>1</default>
									</select>
									<select id='4'>
										<field>pagelen</field>
										<values>
											<value>10</value>
											<value>100</value>
											<value>1000</value>
											<value>10000</value>
										</values>
										<default>10</default>
									</select>
								</root>";
								
				$PHPLIBPATH = getenv("PHPLIBPATH");
				$SSDBPATH = getenv("SSDBPATH");
				$SSDBNAME = getenv("SSDBNAME");

				if ($PHPLIBPATH == "") {
					trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);	
				}

				set_include_path($PHPLIBPATH);

				include_once 'ui_utils.php';
				include_once 'db_utils.php';
				include_once 'xml2html2.php';
				include_once 'url.php';

				$api = php_sapi_name();

				if ($api=='cli') {
					$SSDBNAME = $argv[1];
					$SSDB = $SSDBPATH."/".$SSDBNAME;
				}
				else {
					$SSDB = $SSDBPATH."/".$SSDBNAME;
				}

				if ($SSDBNAME == "" or (file_exists($SSDB) == False)) {
					echo "a valid database name must be passed in as an argument";
				}
				
				$spanclass = NULL;
				$class=NULL;
				$spanclass = "custom-dropdown custom-dropdown--white";
				$class = "custom-dropdown__select custom-dropdown__select--white";

				echo "<div id='one'>";
				gethtmlxmlselect($xml,$_GET,TRUE,FALSE,$spanclass,$class);
				echo "</div>";				
				
				echo "<div id='two'>";
				gethtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],
							TRUE,FALSE,$spanclass,$class);
				echo "<br><br>";
				gethtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],
							TRUE,FALSE,$spanclass,$class);
				echo "<br><br>";
				gethtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],
							TRUE,FALSE,$spanclass,$class);
				echo "<br><br>";
				gethtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],
							TRUE,FALSE,$spanclass,$class);
				echo "<br><br>";
				gethtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],
							TRUE,FALSE,$spanclass,$class);
				
				echo "</div>";
				?>
</div>
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
		//$url = buildurl('http://blackbear:8080/',$args);
		$url = buildurl($SSRESTURL,$args);
	}

	$token = getcurl($url);
echo "<br><br>";
echo "<div id='five'>";

draw($token,$args);
echo "</div>";
}

?>