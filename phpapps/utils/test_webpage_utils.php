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
test_drawxmlselectpopout
test_drawdbselectpopout  							1 popout with more than one select element on it
test_draw2multiselectpopout					1 popout with 2 multi-choice (checkboxes) on it
test_drawmultiselectpopout                	1 popout with 1 multi-choice (checkboxes) on it
test_drawmultiselectpopout_many			2 popouts with 1 multi-choice (checkboxes) on each
test_drawmixedpopout								1 popout with both select and multi-choice elements on it
test_drawtable
test_drawpivot
test_drawtextinputpopup
test_drawserverpopout
test_drawmenu

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

class test_popout 	extends PHPUnit_Framework_TestCase 
{
	public function test_bottompopout()
	{
		ob_start(); 
		global $localip;
		
		
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px","bottom");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_bottom.php',
										'server_name' => "$localip");
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow','cnstr_period' => 'select distinct name from period');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('1','wideswitch',\$_GET,\$poparr,'datacolumns',1,'bottom');
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		

		//jsphpbridge('popout_bottom.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_bottom.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
public function test_topbottompopout()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px","bottom");
		jsslideoutinit(2,"600px","top");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
	
			\$globals = array('script_name' => 'popout_topbottom.php',
										'server_name' => "$localip");
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow','cnstr_period' => 'select distinct name from period');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('1','wideswitch',\$_GET,\$poparr,'datacolumns',1,"bottom");
			drawpopout(\$args);
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow','cnstr_period' => 'select distinct name from period');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('2','wideswitch',\$_GET,\$poparr,'datacolumns',1,"top");
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_topbottom.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_topbottom.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}
class test_menu_update extends PHPUnit_Framework_TestCase 
{
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dedit.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(2,"350px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_menu_update.php',
										'server_name' => "$localip",
										 'editbutton' => 'editsubmit');
										 			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');			
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		echo "<body><table><tr><td id='mytd'>booboo<p id='02B1EEDC' hidden /></td></tr></table></body>";

		//jsphpbridge('popout_menu_update.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_menu_update.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawmenu extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		// draw popout from server provided content
		ob_start(); 
		global $localip;
									
		jsinitpivot('dmenu.js');// initial includes; main js callback routines that recall page on change and base style sheets
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			
			initpage(FALSE);			

			\$menuxml  = "<root><item name='foo'><id>linka</id><link>foobar.php</link></item><item name='bar'><id>linkb</id><jscript>window.location = 'foobar.php'</jscript></item></root>";
			getchtmlxmlmenu2(\$menuxml,"label");

		?>
PHP;
		echo $str;
		
		echo "<body><table><tr><td id='mytd'>booboo<p id='1.1.1.1.1' hidden /></td></tr></table></body>";

		//jsphpbridge('popout_server.php');
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/menu.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}
class test_drawserverpopout extends PHPUnit_Framework_TestCase
{
	// popout with input widgets passed from server
	// new message window
	public function test_()
	{
		// draw popout from server provided content
		ob_start(); 
		global $localip;
									
		jsinitpivot('dnew.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_server.php',
										'server_name' => "$localip");
			
			\$getargs = array('source_value' => 'subject', 'source_type' => 'new');
			\$serverdefnarr =  array();
			\$poparr = array('drawservercontent' => \$serverdefnarr);
			\$args = Array('1','contain',\$getargs,\$poparr,'new',1);
			drawpopout(\$args);
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_server.php');
		jsphpbridge($globals = NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_server.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_js()
	{
		// draw popout from server provided content
		// call server with jscript
		
		ob_start(); 
		global $localip;
									
		jsinitpivot('dnew.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_jsserver.php',
										'server_name' => "$localip");
			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew','class' => 'new');
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_jsserver.php');
		jsphpbridge($globals = NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_jsserver.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_jsentry()
	{
		// uses passed in arg to to create callback fro button
		
		// draw popout from server provided content
		// call server with jscript
		// add a button that collects input and calls a function
		
		$callback = "\"var p= document.createElement('p');p.id='doodah';p.innerHTML= 'foobbaaaahhhrr';document.body.appendChild(p);\"";
			
		ob_start(); 
		global $localip;
									
		jsinitpivot('dnew.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			
			\$globals = array('script_name' => 'popout_jsserverentry.php',
										'server_name' => "$localip");
										 
			initpage();
			\$widgetdefnarr =  array(type => 'submit', id => 'submitfoo', label => 'submit', jscallback => $callback);			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew');
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_jsserverentry.php');
		jsphpbridge($globals = NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_jsserverentry.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_jsentry_externalfilecallback()
	{
		// uses dnew.js to create callback fro button
		
		// draw popout from server provided content
		// call server with jscript
		// add a button that collects input and calls a function
		
		ob_start(); 
		global $localip;
									
		jsinitpivot('dnew.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_jsserverentry_ext.php',
										'server_name' => "$localip");
			
			\$widgetdefnarr =  array(type => 'submit', id => 'submitfoo', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew');
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_jsserverentry_ext.php');
		jsphpbridge($globals = NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_jsserverentry_ext.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_jsentry_externalfilecallback_cls()
	{
		// uses dnew.js to create callback fro button
		
		// draw popout from server provided content
		// call server with jscript
		// add a button that collects input and calls a function
		
		ob_start(); 
		global $localip;
									
		jsinitpivot('dnew.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_jsserverentry_ext_cls.php',
										'server_name' => "$localip",
										 'newbutton'=>'newsubmit');
										 
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_jsserverentry_ext_cls.php','newsubmit');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_jsserverentry_ext_cls.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_jsentry_externalfilecallback_cls_edit()
	{
		// this is actually the same as the dedit.php page
		
		// uses dnew.js to create callback fro button
		
		// draw popout from server provided content
		// call server with jscript
		// add a button that collects input and calls a function
		
		ob_start(); 
		global $localip;
									
		jsinitpivot('dedit.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
										 			
			\$globals = array('script_name' => 'popout_edit.php',
										'server_name' => "$localip",
										 'editbutton'=>'editsubmit');
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');			
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_edit.php');
		jsphpbridge($globals = NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_edit.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
		
 public function test_jsentry_externalfilecallback_cls_2popouts()
	{
		// uses dnew.js to create callback fro button
		
		// draw popout from server provided content
		// call server with jscript
		// add a button that collects input and calls a function
		
		// each popout behaves differently which is configured by class and hooked in dnew.js
		
		ob_start(); 
		global $localip;
									
		jsinitpivot('dnew.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
		jsslideoutinit(2,"450px");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_jsserverentry_ext_cls2p.php',
										'server_name' => "$localip",'newbutton' => 'newsubmit');
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$widgetdefnarr = array('fields' => array("student" => "source_value"));
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr, 
												'drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
			drawtable(\$_GET);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_jsserverentry_ext_cls2p.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_jsserverentry_ext_cls2p.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}	

class test_drawserverpopout_mixed extends PHPUnit_Framework_TestCase
{
	function test_()
	{
		// edit and new popout mixed to test that selectors are specific enough
	ob_start(); 
	global $localip;
									
		jsinitpivot('dmixed.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px","top");
		jsslideoutinit(2,"450px","top");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_server_mixed.php',
										'server_name' => "$localip",
										 'editbutton'=>'editsubmit',
										 'newbutton'=>'newsubmit');
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');	
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_server_mixed.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_server_mixed.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	   
	}
	
function test_with_pivot()
	{
		// edit and new popout mixed to test that selectors are specific enough
	ob_start(); 
	global $localip;
									
		jsinitpivot('dmixed_wpivot.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px","top");
		jsslideoutinit(2,"450px","top");
		jsslideoutinit(3,"650px","top");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_server_mixed_wpivot.php',
										'server_name' => "$localip",
										 'editbutton'=>'editsubmit',
										 'newbutton'=>'newsubmit');
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$widgetdefnarr =  array('fields' =>array("student" => "source_value"));
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr, 
												'drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');	
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('3','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
			drawtable(\$_GET);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_server_mixed_wpivot.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_server_mixed_wpivot.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	   
	}
		
function test_with_pivot_criteria()
	{
		// edit and new popout mixed to test that selectors are specific enough
	ob_start(); 
	global $localip;
								
									
		jsinitpivot('dmixed_wpivot_crit.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px","top");
		jsslideoutinit(4,"450px","top");
		jsslideoutinit(5,"650px","top");
		jsslideoutinit(2,"250px","bottom");
		jsslideoutinit(3,"450px","bottom");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_server_mixed_wpivot_crit.php',
										'server_name' => "$localip",
										 'editbutton'=>'editsubmit',
										 'newbutton'=>'newsubmit');
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$widgetdefnarr =  array('fields' =>array("student" => "source_value"));
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr, 
												'drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');	
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'edit',1,'bottom');
			drawpopout(\$args);
			
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('3','contain',\$_GET,\$poparr,'new',1,'bottom');
			drawpopout(\$args);
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow',
															  'cnstr_period' => 'select distinct name from period',
															  'cnstr_subject' => 'select distinct name from subject');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('4','wideswitch',\$_GET,\$poparr,'filters',2,"top");
			drawpopout(\$args);
			
			\$checkdefnarr = array("status" => "status","subject" => "subject","adult" => "adult",
										           "student" => "student","period" => "period","dow" => "dow",
											   		 "record" => "record","recordtype" => "recordtype","id" => "id");
			\$poparr = array('drawcheckbox' => \$checkdefnarr);
			\$args = Array('5','contain',\$_GET,\$poparr,'datacolumns',2,"top");
			drawpopout(\$args);
			
			drawtable(\$_GET);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_server_mixed_wpivot_crit.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_server_mixed_wpivot_crit.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	   
	}

function test_with_pivot_criteria_search()
	{
		// edit and new popout mixed to test that selectors are specific enough
	ob_start(); 
	global $localip;
									
		jsinitpivot('dmixed_wpivot_crit_search.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px","top");
		jsslideoutinit(4,"450px","top");
		jsslideoutinit(5,"650px","top");
		jsslideoutinit(2,"250px","bottom");
		jsslideoutinit(3,"450px","bottom");
		jsslideoutinit(6,"650px","bottom");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_server_mixed_wpivot_crits.php',
										'server_name' => "$localip",
										 'editbutton'=>'editsubmit',
										 'newbutton'=>'newsubmit');
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$widgetdefnarr =  array('fields' =>array("student" => "source_value"));
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr, 
												'drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1,'top');
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');	
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'edit',1,'bottom');
			drawpopout(\$args);
			
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('3','contain',\$_GET,\$poparr,'new',1,'bottom');
			drawpopout(\$args);
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow',
															  'cnstr_period' => 'select distinct name from period',
															  'cnstr_subject' => 'select distinct name from subject');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('4','wideswitch',\$_GET,\$poparr,'filters',2,"top");
			drawpopout(\$args);
			
			\$checkdefnarr = array("status" => "status","subject" => "subject","adult" => "adult",
										           "student" => "student","period" => "period","dow" => "dow",
											   		 "record" => "record","recordtype" => "recordtype","id" => "id");
			\$poparr = array('drawcheckbox' => \$checkdefnarr);
			\$args = Array('5','contain',\$_GET,\$poparr,'datacolumns',2,"top");
			drawpopout(\$args);
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml",'xmlfileparam' => 'dsearch',"class" => "search");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr);
			\$args = Array('6','contain',\$_GET,\$poparr,'search',1,'bottom');
			drawpopout(\$args);	
		
			drawtable(\$_GET);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_server_mixed_wpivot_crits.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_server_mixed_wpivot_crits.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	   
	}
	
function test_with_pivot_criteria_view()
	{
		// edit and new popout mixed to test that selectors are specific enough
	ob_start(); 
		global $localip;
		
		jsinitpivot('dmixed_wpivot_crit_view.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px","top");
		jsslideoutinit(4,"450px","top");
		jsslideoutinit(5,"650px","top");
		jsslideoutinit(2,"250px","bottom");
		jsslideoutinit(3,"450px","bottom");
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_server_mixed_wpivot_critv.php',
										 'server_name' => "$localip",
										 'editbutton'=>'editsubmit',
										 'newbutton'=>'newsubmit',
										 'viewbutton'=>'viewsubmit');
			
			\$widgetdefnarr =  array(type => 'submit', id => 'viewsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml",'xmlfileparam' => 'dview',"class" => "view");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'view',1);
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');	
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'edit',1,'bottom');
			drawpopout(\$args);
			
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('3','contain',\$_GET,\$poparr,'new',1,'bottom');
			drawpopout(\$args);
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow',
															  'cnstr_period' => 'select distinct name from period',
															  'cnstr_subject' => 'select distinct name from subject');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('4','wideswitch',\$_GET,\$poparr,'filters',2,"top");
			drawpopout(\$args);
			
			\$checkdefnarr = array("status" => "status","subject" => "subject","adult" => "adult",
										           "student" => "student","period" => "period","dow" => "dow",
											   		 "record" => "record","recordtype" => "recordtype","id" => "id");
			\$poparr = array('drawcheckbox' => \$checkdefnarr);
			\$args = Array('5','contain',\$_GET,\$poparr,'datacolumns',2,"top");
			drawpopout(\$args);
		
			drawtable(\$_GET);
			
		?>
PHP;
		echo $str;

		//jsphpbridge('popout_server_mixed_wpivot_critv.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_server_mixed_wpivot_critv.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	   
	}
}

class test_drawview extends PHPUnit_Framework_TestCase
{
	// toggleable pivot/search dropdown
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dview.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
		jsslideoutinit(2,"450px");
		jsslideoutinit(3,"400px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
		
			\$globals = array('script_name' => 'view.php',
										'server_name' => "$localip",
										  'viewbutton'=>'viewsubmit',);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'viewsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml",'xmlfileparam' => 'dview',"class" => "view");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'view',1);

			drawpopout(\$args);
			drawtable(\$_GET);

		?>
PHP;
		echo $str;

		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/view.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}
			
class test_drawpivot extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px");
		jsslideoutinit(2,"450px");
		jsslideoutinit(3,"400px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
		
			\$globals = array('script_name' => 'pivot.php',
										'server_name' => "$localip");
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$widgetdefnarr =  array('fields' =>array("student" => "source_value"));
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr, 
												'drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1);
			drawpopout(\$args);
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow',
															  'cnstr_period' => 'select distinct name from period',
															  'cnstr_subject' => 'select distinct name from subject');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('3','wideswitch',\$_GET,\$poparr,'filters',2);
			drawpopout(\$args);
			
			\$checkdefnarr = array("status" => "status","subject" => "subject","adult" => "adult",
										           "student" => "student","period" => "period","dow" => "dow",
											   		 "record" => "record","recordtype" => "recordtype","id" => "id");
			\$poparr = array('drawcheckbox' => \$checkdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'datacolumns',2);
			drawpopout(\$args);
			
			\$getargs = array('source_value' => 'Clayton', 
												 'ztypes' => 'subject,student',
												 'source_type' => 'student',
												 'xaxis' => 'period',
												 'yaxis' => 'dow');

			drawtable(\$_GET);
			
		?>
PHP;
		echo $str;

		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/pivot.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

			
class test_drawtable extends PHPUnit_Framework_TestCase
{
	// draw some tables by getting XML from REST service (need to run prod.sh)
	public function test_()
	{
		ob_start(); 
		global $localip;
											
		$str = <<<PHP
		<html><head><head><html>
		<?php
		
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage(FALSE);
		
			\$getargs = array('source_value' => 'Clayton', 
												 'ztypes' => 'subject,student',
												 'source_type' => 'student',
												 'xaxis' => 'period',
												 'yaxis' => 'dow');
			drawtable(\$getargs);
		?>
PHP;
		echo $str;

		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/table.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_defaultargs()
	{
		// $_GET is insufficient to get a response out of the web service
		// $_GET is indicative of what gets filled out by webpage as default only
		ob_start(); 
		global $localip;
											
		$str = <<<PHP
		<html><head><head><html>
		<?php
		
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage(FALSE);
		
			\$getargs = array('source_type' => 'student',
												 'xaxis' => 'period',
												 'yaxis' => 'dow');
			drawtable(\$getargs);
		?>
PHP;
		echo $str;

		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/table_noargs.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_noztype()
	{
		// $_GET is insufficient to get a response out of the web service
		// $_GET is indicative of what gets filled out by webpage as default only
		ob_start(); 
		global $localip;
											
		$str = <<<PHP
		<html><head><head><html>
		<?php
		
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage(FALSE);
		
			\$getargs = array('source_type' => 'student',
											    'source_value' => 'Clayton',
												 'xaxis' => 'period',
												 'yaxis' => 'dow');
			drawtable(\$getargs);
		?>
PHP;
		echo $str;

		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/table_noztypes.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawmixedpopout extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_mixed.php',
										'server_name' => "$localip");
										 
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow','cnstr_period' => 'select distinct name from period');
			\$widgetdefnarr =  array("fields" => array("subject" => "cnstr_subject","student" => "cnstr_student"));
			\$poparr = array('drawdbselects' => \$widgetdefnarr,'drawmultiselect' => \$multiselectarr);
			\$args = Array('1','wideswitch',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_mixed.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_mixed.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawxmlselectpopout extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_xml.php',
										'server_name' => "$localip");
				
			\$widgetdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$poparr = array('drawxmlselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_xml.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_xml.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	// popout with multiple selects on it and a special class
	public function test_class()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_xmlcls.php',
										'server_name' => "$localip");
				
			\$widgetdefnarr =  array("xmlfile" => "dropdowns.xml","class" => "foo");
			\$poparr = array('drawxmlselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_xmlcls.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_xmlcls.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawbuttonpopout extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start(); 
		global $localip;		
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		//$callback = "\"console.log('fooblahhhhh')\"";
		//$callback = "\"alert('fooblahhhhh')\"";
		$callback = "\"var p= document.createElement('p');p.id='doodah';p.innerHTML= 'foobbaaaahhhrr';document.body.appendChild(p);\"";
	
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_button.php',
										'server_name' => "$localip");

			\$widgetdefnarr =  array(type => 'submit', id => 'submitfoo', label => 'submit', jscallback => $callback);
			\$poparr = array('drawbutton' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
				
		//jsphpbridge('popout_button.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_button.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawdbselectpopout extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start();
		global $localip; 
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_select.php',
										'server_name' => "$localip");
			
			\$widgetdefnarr =  array('fields' => array("subject" => "cnstr_subject","dow" => "cnstr_dow"));
			\$poparr = array('drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_select.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_select.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
	
	public function test_class()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_select.php',
										'server_name' => "$localip");
										 
			\$widgetdefnarr =  array('fields' => array("subject" => "cnstr_subject","dow" => "cnstr_dow"),'class' => "foo");
			\$poparr = array('drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_selectcls.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_selectcls.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_drawcheckboxpopout extends PHPUnit_Framework_TestCase
{
	//checkboxes this will create ztypes
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_check.php',
										'server_name' => "$localip");
			
			\$checkdefnarr = array("status" => "status","subject" => "subject","adult" => "adult",
										           "student" => "student","period" => "period","dow" => "dow",
											   		 "record" => "record","recordtype" => "recordtype","id" => "id");
			
		
			\$poparr = array('drawcheckbox' => \$checkdefnarr);
			\$args = Array('1','containswitch',\$_GET,\$poparr,'datacolumns',1);

			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_check.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_check.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_draw2multiselectpopout extends PHPUnit_Framework_TestCase
{
	// 2 multiselect on one popout
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'popout_dow_period.php',
										'server_name' => "$localip");			
										 
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow','cnstr_period' => 'select distinct name from period');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('1','wideswitch',\$_GET,\$poparr,'datacolumns',1);
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_dow_period.php');
		jsphpbridge($globals=NULL);
		
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
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();

	
			\$globals = array('script_name' => 'popout_dow.php',
										'server_name' => "$localip");			
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow');			
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('1','wideswitch',\$_GET,\$poparr,'datacolumns',1);
			
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		jsphpbridge($globals=NULL);
		
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
		global $localip;
									
		jsinitpivot('dsearch.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"200px");
		jsslideoutinit(2,"600px");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
	
			\$globals = array('script_name' => 'popout_many.php',
										'server_name' => "$localip");
										 
			\$args = Array('1','wideswitch',\$_GET,'drawmultiselect','datacolumns','select distinct name from dow','cnstr_dow',1);
			drawpopout(\$args);
			\$args = Array('2','wideswitch',\$_GET,'drawmultiselect','datacolumns','select distinct name from period','cnstr_period',1);
			drawpopout(\$args);
		?>
PHP;
		echo $str;
		
		//jsphpbridge('popout_many.php');
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/popout_many.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}
  
class test_drawsearch extends PHPUnit_Framework_TestCase
{
	public function test_()
	{
		ob_start(); 
		global $localip;
		
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

class test_drawapp extends PHPUnit_Framework_TestCase
{
	// popout with multiple selects on it
	public function test_()
	{
		ob_start(); 
		global $localip;
									
		jsinitpivot('dapp.js');// initial includes; main js callback routines that recall page on change and base style sheets
		jsslideoutinit(1,"250px","top");
		jsslideoutinit(2,"450px","top");
		jsslideoutinit(3,"250px","bottom");
		jsslideoutinit(4,"650px","top");
		jsslideoutinit(5,"450","bottom");
		
		$str = <<<PHP
		<?php
			include_once 'bootstrap.php';
			include_once 'webpage_utils.php';
			initpage();
			
			\$globals = array('script_name' => 'app.php',
										'server_name' => "$localip",
										 'editbutton'=>'editsubmit',
										 'newbutton'=>'newsubmit');
			
			\$xmlselectdefnarr =  array("xmlfile" => "dropdowns.xml");
			\$widgetdefnarr =  array('fields' =>array("student" => "source_value"));
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr, 
												'drawdbselects' => \$widgetdefnarr);
			\$args = Array('1','contain',\$_GET,\$poparr,'main',1,"top");
			drawpopout(\$args);
			
			\$multiselectarr = array( 'cnstr_dow' => 'select distinct name from dow',
															  'cnstr_period' => 'select distinct name from period',
															  'cnstr_subject' => 'select distinct name from subject');
			\$poparr = array('drawmultiselect' => \$multiselectarr);
			\$args = Array('3','wideswitch',\$_GET,\$poparr,'filters',2,"bottom");
			drawpopout(\$args);
			
			\$checkdefnarr = array("status" => "status","subject" => "subject","adult" => "adult",
										           "student" => "student","period" => "period","dow" => "dow",
											   		 "record" => "record","recordtype" => "recordtype","id" => "id");
			\$poparr = array('drawcheckbox' => \$checkdefnarr);
			\$args = Array('2','contain',\$_GET,\$poparr,'datacolumns',2,"top");
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'editsubmit', label => 'submit');			
			\$xmlinputdefnarr =  array('xmlfile' => 'inputs.xml','xmlfileparam' => 'dedit',"class" => "edit");
			\$poparr = array('drawxmlinputs' => \$xmlinputdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('4','contain',\$_GET,\$poparr,'update',1,"top");
			drawpopout(\$args);
			
			\$widgetdefnarr =  array(type => 'submit', id => 'newsubmit', label => 'submit');			
			\$xmlselectdefnarr =  array('xmlfile' => 'dropdowns.xml','xmlfileparam' => 'dnew',"class" => "new");
			\$poparr = array('drawxmlselects' => \$xmlselectdefnarr,'drawbutton' => \$widgetdefnarr);
			\$args = Array('5','contain',\$_GET,\$poparr,'new',1,'bottom');
			drawpopout(\$args);
			
			drawtable(\$_GET);
		?>
PHP;
		echo $str;

		//jsphpbridge("app.php");
		jsphpbridge($globals=NULL);
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/app.php",$result,"w");
	   //$this->assertEquals($this->expected_result,$result);
	}
}

class test_misc 	extends PHPUnit_Framework_TestCase 
{
	public function test_jsphpbridge()
	{
		ob_start(); 
		global $localip;
										 
		$str = <<<PHP
		<?php
			include_once 'webpage_utils.php';
		\$globals = array('script_name' => 'phpbridge.php',
										'server_name' => "$localip",
										 'foo' => 'bar');
		?>
PHP;
		echo $str;
		
		echo "<html><body></body></html>";
							 
		jsphpbridge($globals=NULL);
		

				$str = <<<JS
<script>
var p= document.createElement('p');
p.id=Globals.foo;
document.body.appendChild(p);
</script>		
JS;
		echo $str;
		
		$result = ob_get_contents();
		ob_end_clean();		
		
		writetofile("/var/www/html-dev/phpbridge.php",$result,"w");
	}
}
set_error_handler("handleError");
   
$localip = getHostByName(getHostName());

try {
	/*testrunner("drawmultiselectpopout");
	testrunner("draw2multiselectpopout");
	testrunner("drawmultiselectpopout_many");
	testrunner("drawdbselectpopout");
	testrunner("drawmixedpopout");
	testrunner("drawtable");
	testrunner("drawpivot");
	testrunner("drawcheckboxpopout");
	testrunner("drawxmlselectpopout");
	testrunner("drawbuttonpopout");
	testrunner("drawserverpopout");
	
	testrunner("drawmenu");
	testrunner("menu_update");
	testrunner("drawapp");
	testrunner("popout");
	testrunner("drawview");
	testrunner("misc");*/
	testrunner("drawserverpopout_mixed");
	 
	 
	 
} catch (Exception $e) {
    echo 'Caught exception: ',  $e->getMessage(), "\n";
}

?>