<?php

/* to run these tests
// these need sudo ln -s html-dev/ html
	27  . ~/.bashrc
   530  export SSDBNAME=/Users/burtnolej/Development/pythonapps/clean/db/fucia.sqlite
   529  php ./test_webpage_utils.php 
	output goes to /var/www/html/tmp.php which is linked to /Users/burtnolej/Development/pythonapps/phpapps/utils/tmp.html   
	access in browser 0.0.0.0/tmp.php
   */
  
/* whats in this file 

test_drawselectpopout  								1 popout with more than one select element on it
test_draw2multiselectpopout					1 popout with 2 multi-choice (checkboxes) on it
test_drawmultiselectpopout                	1 popout with 1 multi-choice (checkboxes) on it
test_drawmultiselectpopout_many			2 popouts with 1 multi-choice (checkboxes) on each
test_drawmixedpopout								1 popout with both select and multi-choice elements on it

*/



$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

set_include_path($PHPLIBPATH);
require_once 'autoload.php';

include_once 'ui_utils.php';
include_once 'utils_error.php';
include_once 'utils_utils.php';
include_once 'test_utils.php';
include_once 'webpage_utils.php';


class test_drawselectpopout extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start(); 
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$widgetdefnarr =  array("subject" => "cnstr_subject","dow" => "cnstr_dow");
			\$args = Array('1','contain',\$_GET,'drawdbselects','datacolumns','lesson',\$widgetdefnarr);
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		jsphpbridge('popout_select.php');
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_select.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_draw2multiselectpopout extends PHPUnit_Framework_TestCase
{
	// 2 multiselect on one popout
	public function test_()
	{
		ob_start(); 
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow','cnstr_period' => 'select distinct name from period');
			\$args = Array('1','wideswitch',\$_GET,'drawmultiselect','datacolumns',\$multiselectarr,1);
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		jsphpbridge('popout_dow_period.php');
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_dow_period.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawmultiselectpopout extends PHPUnit_Framework_TestCase
{
	// 1 multiselect popout
	public function test_()
	{
		ob_start(); 
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow');
			\$args = Array('1','wideswitch',\$_GET,'drawmultiselect','datacolumns',\$multiselectarr,1);
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		jsphpbridge('popout_dow.php');
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_dow.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawmultiselectpopout_many extends PHPUnit_Framework_TestCase
{
	// 2 popouts
	public function test_()
	{
		ob_start(); 
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"200px");
		jsslideoutinit(2,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			\$args = Array('1','wideswitch',\$_GET,'drawmultiselect','datacolumns','select distinct name from dow','cnstr_dow',1);
			drawpopout(\$args);
			\$args = Array('2','wideswitch',\$_GET,'drawmultiselect','datacolumns','select distinct name from period','cnstr_period',1);
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		jsphpbridge('popout_many.php');
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_many.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawpivot extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		ob_start(); 
											
		jsinitpivot('dpivot.js');// initial includes; main js callback routines that recall page on change and base style sheets
		phpinit('drawpivot'); // main php code
		jsphpbridge('wideswitch'); // bridge between php and js code
		jsdefer(); // final display of widgets to avoid flicker
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("tmp.html",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}
  
class test_drawsearch extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		ob_start(); 
		
		$getargs = array("source_value" => 'Clayton',
											"ztypes" => "",
											"cnstr_subject" => "",
											"cnstr_dow" => "",
											"cnstr_period" => "",
											"cnstr_student" => "",
											"cnstr_adult" => "",
											"cnstr_prep" => "",
											"cnstr_source" => "",
											"cnstr_recordtype" => "",
											"handle1" => 'in',
											"handle2" => 'in',
											"handle3" => 'in',
											"last_source_value" => ""
											);
		$str = <<<JS
<html>
<head>

<link rel="stylesheet" type="text/css" href="css/select.css" />
<link rel="stylesheet" type="text/css" href="css/div.css" />
<link rel="stylesheet" type="text/css" href="css/switch.css" />
<link rel="stylesheet" type="text/css" href="css/menu.css" />
<link rel="stylesheet" type="text/css" href="plain.css" />"

<!--style> body { display:none;} </style-->
<script data-main="js/localdsearch.js" src="js/require.js"></script>
</head>

JS;
		echo $str;

		echo "<body>";
		drawsearch($getargs);
		echo "</body></html>";

$str = <<<JS
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
 
 //setTimeout(function() {
 		//els = document.body.setAttribute("style","display: block;");
  	//},150);
 		 		
  		setElementStyle('contain','display','block',150);
		setElementStyle('containswitch','display','block',150);
		setElementStyle('wideswitch','display','block',150);
		setElementStyle('borderoff','display','block',150);
		 </script>
JS;
echo $str;



		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("tmp.html",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

set_error_handler("handleError");
   
try {
	
	/* drawpivot */
	//testrunner("drawsearch");
	//testrunner("drawpivot");
	//testrunner("drawmultiselectpopout");
	testrunner("draw2multiselectpopout");
	//testrunner("drawmultiselectpopout_many");
	
	testrunner("drawselectpopout");
	
	
	
	
	
} catch (Exception $e) {
    echo 'Caught exception: ',  $e->getMessage(), "\n";
}

?>