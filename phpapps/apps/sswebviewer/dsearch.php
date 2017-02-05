<!DOCTYPE html>
<html lang="en">

 <!--head>
 		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
        
<script src="jquery-3.1.1.js"></script>
<script src="stylesheets.js"></script>

</html>

<html-->
<script src="jquery-3.1.1.js"></script>

<script data-main="js/dsearch.js" src="js/require.js"></script>
<!--script src="stylesheets.js"></script-->

<script>$('head').html('<link rel="stylesheet" type="text/css" href="css/select.css" /><link rel="stylesheet" type="text/css" href="css/div.css" /><link rel="stylesheet" type="text/css" href="css/switch.css" /><link rel="stylesheet" type="text/css" href="css/menu.css" />');
</script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$args= Array('hidden' => 'true');
	getchtmlinput('',"handle1",$_GET['handle1'],$args);
	getchtmlinput('',"handle2",$_GET['handle2'],$args);
	getchtmlinput('',"handle3",$_GET['handle3'],$args);
	
	$args= Array('hidden' => 'true');
	getchtmlinput('','last_source_value',$_GET['source_value'],$args);
	
	$func = function($arr) {	
		$getargs = $arr[0];
		$SSDB = $arr[1];
	//$func = function() {
		//global $SSDB;
		$xml = file_get_contents("dropdowns.xml");
		getxmlhtmlcselect($xml,$_GET,'label','dsearch');		
	};
	//gethtmlpopoutdiv("main",$func,"slide-out-div-top3 contain","handle3 pol3");	
	gethtmlpopoutdiv("main",$func,Array($getargs,$SSDB),"slide-out-div-top3 contain","handle3 pol3");	
	
	$func = function($arr) {	
		$getargs = $arr[0];
		$SSDB = $arr[1];
	//$func = function() {
		//global $SSDB;
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],array("distinct" => false,"label" => "subject"));
		getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],array("distinct" => false,"label" => "dow"));
		getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],array("distinct" => false,"label" => "period"));
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],array("distinct" => false,"label" => "student"));
		getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],array("distinct" => true,"label" => "teacher"));
	};
	//gethtmlpopoutdiv("filters",$func,"slide-out-div-top2 contain","handle2 pol2");	
	gethtmlpopoutdiv("filters",$func,Array($getargs,$SSDB),"slide-out-div-top2 contain","handle2 pol2");	
	
	$func = function($arr) {		
		$getargs = $arr[0];
		$SSDB = $arr[1];
	//$func = function() {
	//	global $SSDB;

		if ($_GET['source_value'] == "") {
			$_GET['source_value'] = "lesson";
		};
		
		// get the list of possible columns from the database for this source_type
		$cols = gettablecolumns($SSDB,$_GET['source_value']);
		
		// check if source_value has been changed since last page load
		if ($_GET['last_source_value'] 	<> $_GET['source_value']) {
			
			// source_value has been changed so set checkbox 'on' to list of possible columns
			// first load for a given source_type is always all columns
			$args = array('checked'=>$cols,'comment' => 'Choose what datafields you want to see in a cell of the grid');
			
			// force the resetting of ztypes as the jquery callback that sets them only fires when 
			// as input element is changed. in this case the change is source_value select
			$_GET['ztypes'] = implode(",",$cols);
		}
		else {
			$args = array('checked'=>explode(",",$_GET['ztypes']),'comment' => 'Choose what datafields you want to see in a cell of the grid');
		}
		      
		foreach ($cols as $col) {			
			getchtmlswitch($col,$col,$args);
		}
		
		echo "</div>";

	};
 	//gethtmlpopoutdiv("datacolumns",$func," slide-out-div-top containswitch  ","handle1 pol1");	
 	gethtmlpopoutdiv("datacolumns",$func,Array($getargs,$SSDB)," slide-out-div-top containswitch  ","handle1 pol1");	
?>

<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script>



<?php

$_GET['parser']="drawform";

/*
	$args = Array('headeronly' => true,'id' => 'table1');
	call_user_func((string)$funcname,$utilsxml,$args,$formats);
	$args = Array('noheader' => true,'id' => 'table2');
	call_user_func((string)$funcname,$utilsxml,$args,$formats);
	*/
	


if(isset($_GET['pagenum'])) {
//if(isset($_GET['ztypes'])) {
	$token =refreshpage();
	echo "<br><br>";
	
	//$args = Array('fixheader' => true);
	echo "<div class='searchgridhdr'>";
	$args = Array('headeronly' => true,'id' => 'table1');
	draw($token,$args);
	echo "</div>";
	
	echo "<div class='searchgrid'>";
	$args = Array('noheader' => true,'id' => 'table2');
	draw($token,$args);
	echo "</div>";
}
?>

<!--script src="afterload.js" defer></script-->
<!--script data-main="js/dsearch.js" src="js/require.js"></script-->

<!--script src="afterload.js"></script-->

 <script>
  
  			setTimeout(function() {
  				els = document.getElementsByClassName('contain');
  				els[0].style.display = "inline";
    			els[1].style.display = "inline";
    			
  				els = document.getElementsByClassName('containswitch');
  				els[0].style.display = "inline";
    			
  				/*els = document.getElementsByClassName('borderoff');
  				els[0].style.display = "inline";
  				
   				els = document.getElementsByClassName('searchgrid');
  				els[0].style.display = "inline";*/
  				
  				
  			},300);

  </script>

     


