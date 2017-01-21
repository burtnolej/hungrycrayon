

<?php
				function initpage() {
					
					global $PHPLIBPATH;
					
					$menuxml =file_get_contents("menus.xml");
									
					getdbinfo();
		
					set_include_path($PHPLIBPATH);
		
					include_once 'ui_utils.php';
					include_once 'db_utils.php';
					include_once 'xml2html2.php';
					include_once 'url.php';
					
					set_stylesheet();
				
					getchtmlxmlmenu2($menuxml,"label");
					
					echo "<div id=\"content\">";
				}
				
				function getdbinfo() {
	
					$GLOBALS['PHPLIBPATH'] = getenv("PHPLIBPATH");
					$GLOBALS['SSDBPATH'] = getenv("SSDBPATH");
					$GLOBALS['SSDBNAME'] = getenv("SSDBNAME");

					if ($GLOBALS['PHPLIBPATH'] == "") {
						trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);	
					}
					
					$api = php_sapi_name();

					if ($api=='cli') {
						$GLOBALS['SSDBNAME'] = $argv[1];
						$GLOBALS['SSDB'] = $GLOBALS['SSDBPATH']."/".$GLOBALS['SSDBNAME'];
					}
					else {
						$GLOBALS['SSDB']= $GLOBALS['SSDBPATH']."/".$GLOBALS['SSDBNAME'];
					}

					if ($GLOBALS['SSDBNAME'] == "" or (file_exists($GLOBALS['SSDB']) == False)) {
						echo "a valid database name must be passed in as an argument";
					}
				}
				
				function flip_source_type() {
					global $_GET;
					
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
					return $source_type;
				}
	
				function set_stylesheet() {
					global $_GET;
					if (in_array('formats',explode(",",$_GET['ztypes']))) {
						//echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"default.css\" />";
						echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"plain.css\" />";
					}
					else {
						echo "<link rel=\"stylesheet\" type=\"text/css\" href=\"plain.css\" />";
					}
				}
				
				function refreshpage() {
					
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
				
					return(getcurl($url));
				}
?>