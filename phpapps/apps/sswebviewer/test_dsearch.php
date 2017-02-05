<!DOCTYPE html>
<html lang="en">

 <head>
 <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>

<link rel="stylesheet" type="text/css" href="css/select.css" />
<link rel="stylesheet" type="text/css" href="css/div.css" />
<link rel="stylesheet" type="text/css" href="css/switch.css" />
<link rel="stylesheet" type="text/css" href="css/menu.css" />
<link rel="stylesheet" type="text/css" href="plain.css" />"

<script data-main="js/localdpivot.js" src="js/require.js"></script>
</head>
</html>


<?php
$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);
include_once 'webpage_utils.php';
drawsearch($_GET);

?>
<script>var Globals = Array(); Globals['script_name']= 'test_dpivot.php'; Globals['server_name'] ='0.0.0.0';</script>

<script>
function setElementStyle(classname,attr,attrval,timeoutlen) {
	setTimeout(function() {
		els = document.getElementsByClassName(classname);
		for (i = 0; i < els.length; i++) {
			els[i].setAttribute("style", attr + ": " + attrval + ";");
		}
  	},timeoutlen);
 }
 
 		setElementStyle('contain','display','block',10);
		setElementStyle('containswitch','display','block',10);
		setElementStyle('wideswitch','display','block',10);
		setElementStyle('borderoff','display','block',10);
		
 </script>

</html>
     


