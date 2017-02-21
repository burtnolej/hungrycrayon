<?php

/*
drawpopout
drawmultiselect
drawdbselects

drawpivot($getargs = []) 
drawsearch($getargs = []) 

*/

$PHPLIBPATH = getenv("PHPLIBPATH");

if ($PHPLIBPATH == "") {
	trigger_error("Fatal error: env PHPLIBPATH must be set", E_USER_ERROR);
}

$SSDBPATH = getenv("SSDBPATH");
set_include_path($PHPLIBPATH);

include_once 'db_utils.php';
include_once 'utils_xml.php';

function drawtable($getargs) {
	
		$result=refreshpage($getargs);

			$xml = $result['xml'];
			$url = $result['url'];
			
			$func = function() use ($xml,$url,$getargs) {
				$args = Array('noheader' => true,'id' => 'table2');
				
				if ($xml == "-1") {
					echo "ztype".$url;
				}
				elseif ($xml == "not found") {
					echo "ztype".$url;
				}
				else {
					draw($xml,$getargs);
				}
			};
	
			gethtmldiv("title blah blah",$func,"table","divlabel");	
}

function drawservercontent($getargs,$serverdefarr,$maxy) {
	
	$result=refreshpage($getargs);
	$xml = $result['xml'];
	$url = $result['url'];
		
	draw($xml,$getargs);

}

function drawpopout($args) {
		
	$popoutnum = $args[0]; // internal css class used by the actual popout
	$popoutstylename = $args[1]; // internal css class used by the widgets in the popout
	$getargs = $args[2]; // $_GET params from the URL
	$htmlfuncarr = $args[3]; // function to create actual html
	$popoutlabel = $args[4];
	$maxy = $args[5];
	
	if (isset($args[6])) {
		$tablocation = $args[6];
	}
	else {
		$tablocation = 'top';
	}
		
	$args= Array('hidden' => 'true');
	getchtmlinput('',"handle".$popoutnum,$getargs['handle'.$popoutnum],$args);
	
	$args= Array('hidden' => 'true');
	getchtmlinput('','last_source_value',$getargs['source_value'],$args);
	
	gethtmlpopoutdiv($popoutlabel,$getargs,$htmlfuncarr,$popoutnum,$maxy,$popoutstylename,$tablocation);
}


function drawmultiselect($getargs,$multiseldefnarr,$maxy) {
	$firstrow=TRUE;
	foreach ($multiseldefnarr as $field => $query) {
		if (!$firstrow) {
		echo '<hr WIDTH="92%" COLOR="#E0E0E0" SIZE="1">';
		}
		getdbhtmlmultiselect($GLOBALS['SSDB'],$query,$field,Array('checked' => $getargs,'maxy' => $maxy));
		$firstrow=FALSE;
	}
}

function drawdbselects($getargs,$arr,$maxy) {
	
	$dbselectdefnarr = $arr['fields'];

	foreach ($dbselectdefnarr as $dbname => $fieldname) {
		$args = array('comment'=>$comment, 'label' => $dbname,"distinct" => false);		
		
	if (isset($arr['class'])) {
		$args['class'] = $arr['class'];
	}
	
		getchtmldbselect($GLOBALS['SSDB'],$tablename,$dbname,$fieldname,1,$getargs[$fieldname],$args);	
		echo "<br>"; // stacks selects vertically
	}	
}

function drawcheckbox($getargs,$switchdefn,$arr = []) {
	foreach ($switchdefn as $field => $name) {
		$args = array('checked'=>explode(",",$getargs['ztypes']),'comment' => 'blah','single' => TRUE);	
		getchtmlswitch($field,$name,$args);
	}
}

function drawbutton($getargs,$buttondefn,$arr = []) {
		gethtmlbutton($buttondefn['type'],$buttondefn['label'],$buttondefn['id']);
		
		$cb = $buttondefn['jscallback'];
		$str = <<<JS
	 	<script type="text/javascript">
			$(document).ready(function(){
				$("input[id='submitfoo']").on('click',function(){
					$cb;
				}
			)});
		</script>		
JS;
		echo $str;
}

function drawxmlinputs($getargs,$arr,$maxy) {

		$xmlfile = $arr['xmlfile'];
		if (!isset($arr['xmlfileparam'])) { // which bit of xml file to read
			$args = array('starttag' => 'dpivot');
		}
		else {
			$args = array('starttag' => $arr['xmlfileparam']);
		}
		
		if (isset($arr['class'])) { // which bit of xml file to read
			$args['class'] = $arr['class'];
		}
				
		$xml = file_get_contents($xmlfile);
	
		getxmlhtmlinput($xml,$_GET,'edit',"dedit");
}


function drawxmlselects($getargs,$arr,$maxy) {
		$xmlfile = $arr['xmlfile'];
		if (!isset($arr['xmlfileparam'])) { // which bit of xml file to read
			//$xmlfileparam = 'dpivot';
			$args = array('starttag' => 'dpivot');
		}
		else {
			//$xmlfileparam= $arr['xmlfileparam'];
			$args = array('starttag' => $arr['xmlfileparam']);
		}
		
		if (isset($arr['class'])) { // which bit of xml file to read
			//$xmlfileparam = 'dpivot';
			$args['class'] = $arr['class'];
		}
				
		$xml = file_get_contents($xmlfile);
		
		//getxmlhtmlcselect($xml,$getargs,'pivot config',$xmlfileparam);
		getxmlhtmlcselect($xml,$getargs,'pivot config',$args);
}

function drawpivotold($getargs = []) {
	
	/* getargs are the $_GET params passed into the php page; they will be used to provide default values */

	include_once 'bootstrap.php';
	initpage();
	
	$func = function($getargsarray) {		
	
		$getargs = $getargsarray[0];
		
		$xml = file_get_contents("dropdowns.xml");
		getxmlhtmlcselect($xml,$getargs,'pivot config','dpivot');
	};
	gethtmldiv("Main",$func,Array($getargs),"containswitch","divlabel");
	
	$source_type = flip_source_type();
	
	$args = array('comment'=>'What instance of the datatype do you want to view;For instance id the datatype selected was student then Booker could be chosen; if datatype=adult had been chosen, then the list of available adults would be shown in the dropdown','divlabel' => 'View Config','label' => 'Datatype Value');							
	getchtmldbselect($GLOBALS['SSDB'],'lesson',$source_type,"source_value",1,$getargs['source_value'],$args);
						
	$func = function($getargsarray) {
		
		$getargs = $getargsarray[0];
		
		$args = array('checked'=>explode(",",$getargs['ztypes']),'single' => TRUE,'comment' => 'Enables an alternative display that uses color to make it easier to see patterns across grids of data');	
		getchtmlswitch("formats","formats",$args);
		$args['comment'] = 'Rollup multiple entries where they only differ by student, to conserve space on the screen';	
		getchtmlswitch("rollup","rollup",$args); 
		$args['comment'] = 'Display the number of records in each cell instead of the records themselves';
		getchtmlswitch("count","count",$args); 
	};
	gethtmldiv("Visual Config",$func,array($getargs),"containswitch","divlabel");
	
	$func = function($getargsarray) {
		
		$getargs = $getargsarray[0];
		
		$args = array('checked'=>explode(",",$getargs['ztypes']),'single' => TRUE,'comment' => 'Choose what datafields you want to see in a cell of the grid');	
		getchtmlswitch("status","status",$args);
		getchtmlswitch("subject","subject",$args);
		getchtmlswitch("adult","adult",$args);
		getchtmlswitch("student","student",$args);
		getchtmlswitch("period","period",$args);
		getchtmlswitch("dow","dow",$args);
		getchtmlswitch("record","record",$args);
		getchtmlswitch("recordtype","recordtype",$args);
		getchtmlswitch("id","id",$args);
	};
	
	gethtmldiv("datafields",$func,array($getargs),"containswitch","divlabel");		
	
	$func = function($getargsarray) {
		
		$getargs = $getargsarray[0];
		$SSDB = $getargsarray[1];

		$comment = 'Filter the grid to only show rows that match this criteria';
		$args = array('comment'=>$comment, 'label' => 'Subject',"distinct" => false);							
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$getargs['cnstr_subject'],$args);	
		//$args = array('comment'=>$comment, 'label' => 'Weekday',"distinct" => false);			
		//getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$getargs['cnstr_dow'],$args);		
		//$args = array('comment'=>$comment, 'label' => 'Period',"distinct" => false);					
		//getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$getargs['cnstr_period'],$args);
		$args = array('comment'=>$comment, 'label' => 'Student',"distinct" => false);							
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$getargs['cnstr_student'],$args);
		$args = array('comment'=>$comment, 'label' => 'Teacher',"distinct" => false);			
		getchtmldbselect($SSDB,'lesson','adult',"cnstr_adult",1,$getargs['cnstr_adult'],$args);
		$args = array('comment'=>$comment, 'label' => 'Prep');				
		getchtmldbselect($SSDB,'lesson','prep',"cnstr_prep",1,$getargs['cnstr_prep'],$args);		
		$args = array('comment'=>$comment, 'label' => 'Source File');			
		getchtmldbselect($SSDB,'lesson','source',"cnstr_source",1,$getargs['cnstr_source'],$args);
		$args = array('comment'=>$comment, 'label' => 'Record Type','manualvalues' => Array('wp','ap','academic','seminar'));	
		getchtmldbselect($SSDB,'lesson','recordtype',"cnstr_recordtype",1,$getargs['cnstr_recordtype'],$args);
	};
	gethtmldiv("select filters",$func,array($getargs,$GLOBALS['SSDB']),"contain","divlabel");	

	$func = function($getargsarray) {
		
		$getargs = $getargsarray[0];
		$SSDB = $getargsarray[1];

		getdbhtmlmultiselect($SSDB,'select distinct name from dow','cnstr_dow',Array('checked' => $getargs,'maxy' => 10));
		getdbhtmlmultiselect($SSDB,'select distinct name from period','cnstr_period',Array('checked' => $getargs,'maxy' => 10));
	};
	gethtmldiv("select filters",$func,array($getargs,$GLOBALS['SSDB']),"wideswitch","divlabel");	
}

function drawsearch($getargs = []) {
	
	include_once 'bootstrap.php';
	initpage();
	
	$args= Array('hidden' => 'true');
	getchtmlinput('',"handle1",$getargs['handle1'],$args);
	getchtmlinput('',"handle2",$getargs['handle2'],$args);
	getchtmlinput('',"handle3",$getargs['handle3'],$args);
	
	$args= Array('hidden' => 'true');
	getchtmlinput('','last_source_value',$getargs['source_value'],$args);
	
	$func = function($arr) {	
		$getargs = $arr[0];
		$SSDB = $arr[1];
		
		$xml = file_get_contents("dropdowns.xml");
		getxmlhtmlcselect($xml,$getargs,'label','dsearch');		
	};
	gethtmlpopoutdiv("main",$func,Array($getargs,$GLOBALS['SSDB']),"slide-out-div-top3 contain","handle3 pol3");	
	
	$func = function($arr) {		
		$getargs = $arr[0];
		$SSDB = $arr[1];
		
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$getargs['cnstr_subject'],array("distinct" => false,"label" => "subject"));
		getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$getargs['cnstr_dow'],array("distinct" => false,"label" => "dow"));
		getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$getargs['cnstr_period'],array("distinct" => false,"label" => "period"));
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$getargs['cnstr_student'],array("distinct" => false,"label" => "student"));
		getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$getargs['cnstr_adult'],array("distinct" => true,"label" => "teacher"));
	};
	gethtmlpopoutdiv("filters",$func,Array($getargs,$GLOBALS['SSDB']),"slide-out-div-top2 contain","handle2 pol2");	
	
	$func = function($arr) {		
		$getargs = $arr[0];
		$SSDB = $arr[1];

		if ($getargs['source_value'] == "") {
			$getargs['source_value'] = "lesson";
		};
		
		// get the list of possible columns from the database for this source_type
		$cols = gettablecolumns($SSDB,$getargs['source_value']);
		
		// check if source_value has been changed since last page load
		if ($getargs['last_source_value'] 	<> $getargs['source_value']) {
			
			// source_value has been changed so set checkbox 'on' to list of possible columns
			// first load for a given source_type is always all columns
			$args = array('checked'=>$cols,'comment' => 'Choose what datafields you want to see in a cell of the grid');
			
			// force the resetting of ztypes as the jquery callback that sets them only fires when 
			// as input element is changed. in this case the change is source_value select
			$getargs['ztypes'] = implode(",",$cols);
		}
		else {
			$args = array('checked'=>explode(",",$getargs['ztypes']),'comment' => 'Choose what datafields you want to see in a cell of the grid');
		}
		      
		foreach ($cols as $col) {			
			getchtmlswitch($col,$col,$args);
		}
		
		echo "</div>";

	};
 	gethtmlpopoutdiv("datacolumns",$func,Array($getargs,$GLOBALS['SSDB'])," slide-out-div-top containswitch  ","handle1 pol1");	
 	
}

function phpinit($funcname) {
	// main php code 
		$str = <<<PHP
		<?php
		include_once 'bootstrap.php';
		include_once 'webpage_utils.php';
		initpage();
		$funcname(\$_GET);
		?>
PHP;
		echo $str;
}

function jsinitpivot($scriptname) {
		// initial includes; main js callback routines that recall page on change and base style sheets
		$str = <<<JS
<html>
<head>
<script src="jquery.js" type="text/javascript"></script>
<script src="tabSlideOut.js"></script>
<script data-main="js/$scriptname" src="js/require.js"></script>
<link rel="stylesheet" type="text/css" href="css/select.css" />
<link rel="stylesheet" type="text/css" href="css/div.css" />
<link rel="stylesheet" type="text/css" href="css/switch.css" />
<link rel="stylesheet" type="text/css" href="css/menu.css" />
<link rel="stylesheet" type="text/css" href="css/input.css" />
<link rel="stylesheet" type="text/css" href="css/slideout.css" />
</head>

</html>


JS;
		echo $str;
}

function jsslideoutinit($tabnum,$leftpos,$tabloc=NULL) {
	
	if ($tabloc==NULL) {
		$tabloc="top";
	}
	// $leftpos needs to be of the form XXpx
		$str = <<<JS
 <script type="text/javascript">

	$(function(){
        $('.slide-out$tabnum').tabSlideOut({
            tabHandle: '.handle$tabnum',                     //class of the element that will become your tab
            leftPos: '$leftpos',                          //position from left/ use if tabLocation is bottom or top
            tabLocation:'$tabloc',
        });
    });
    
</script>		
JS;
		echo $str;
}


function jsphpbridge($globals) {

		if (!isset($globals['script_name'])) {
			$globals['script_name'] =  'pivot.php';
		}
		if (!isset($globals['server_name'])) {
			$globals['server_name'] =  '0.0.0.0';
		}
		
		// bridge between php and js code
		$str = <<<JS
<script>var Globals = <?php echo json_encode(\$globals); ?>;</script>		
JS;
		echo $str;
}

function jsphpbridgeold($pagename=NULL,$servername=NULL) {

		if ($pagename == NULL ) {
			//$pagename = $_SERVER['PHP_SELF'];
			$pagename = 'pivot.php';
		}
		if ($servername == NULL) {
			//$servername = $_SERVER['SERVER_NAME'];
			$servername = '0.0.0.0';
		}
		
		// bridge between php and js code
		$str = <<<JS
<script>var Globals = <?php echo json_encode(array(
'script_name' => '$pagename',
'server_name' => '$servername')); 
?>;</script>		
JS;
		echo $str;
}

function jsdefer($defertime=150) {
		// final display of widgets to avoid flicker
		// uses Globals.display_list comma delim string to get the element classes to 'display'
$str = <<<JS
<script defer>
function setElementStyle(classname,attr,attrval,timeoutlen) {
	setTimeout(function() {
		els = document.getElementsByClassName(classname);
		for (i = 0; i < els.length; i++) {
			els[i].setAttribute("style", attr + ": " + attrval + ";");
		}
  	},timeoutlen);
 }

 		 	var display_list = Globals.display_list.split(",");
 		 	
 		 	for (i=0;i<display_list.length;i++) {
 		 		setElementStyle(display_list[i],'display','block',$defertime);
 		 	}
 		 	
 		 	console.log("blah");

</script>
JS;
		echo $str;
}
?>