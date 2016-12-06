<!DOCTYPE html>
<html>
<link rel="stylesheet" type="text/css" href="css/select.css" />
<link rel="stylesheet" type="text/css" href="css/div.css" />
<link rel="stylesheet" type="text/css" href="css/switch.css" />

</html>
<html>
			<?php 
			
					$xml = "<root>
									<select id='1'>
										<field>xaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<comment>blah blah blah blah blah</comment>
										<default>period</default>
									</select>
									<select id='2'>
										<field>yaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<comment>blah blah blah blah blah</comment>
										<default>dow</default>
									</select>
									<select id='3'>
										<field>source_type</field>
										<values>
											<value>student</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<comment>blah blah blah blah blah</comment>
										<default>student</default>
									</select>
									<select id='4'>
										<field>source</field>
										<values>
											<value>dbinsert</value>
											<value>56n</value>
											<value>4n</value>
											<value>4s</value>
											<value>5s</value>
											<value>6s</value>
											<value>56n,4n,4s,5s,6s</value>
										</values>
										<comment>blah blah blah blah blah</comment>
										<default>dbinsert</default>
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
				
				getxmlhtmlcselect($xml,$_GET,'this is a div label');

				if (in_array('formats',explode(",",$_GET['ztypes']))) {
					echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"default.css\" />";
				}
				else {
					echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"plain.css\" />";
				}
				
				if (isset($_GET['source_type'])) {
					if ($_GET['source_type'] == "adult") {
						$source_type = 'teacher';
					}
					else {
						$source_type = $_GET['source_type'];
					}
				}
				else {
					$source_type = 'student'; // default
				}
				
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
      		//$url = buildurl('http://blackbear:8080/new',$args);
      		$url = buildurl($SSRESTURL.'new',$args);
      	break;
    		default:
    			//$url = buildurl('http://blackbear:8080/',$args);
				$url = buildurl($SSRESTURL,$args);
		}
	}
	else {
		//$url = buildurl('http://blackbear:8080/',$args);
		$url = buildurl($SSRESTURL,$args);
	}

	$token = getcurl($url);
echo "<br><br>";


draw($token,$args);

}

?>