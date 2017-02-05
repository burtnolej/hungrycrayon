<html>
<script src="jquery-3.1.1.js"></script>

<script data-main="js/dpivot.js" src="js/require.js"></script>
<!--script src="stylesheets.js"></script-->

<script>$('head').html('<link rel="stylesheet" type="text/css" href="css/select.css" /><link rel="stylesheet" type="text/css" href="css/div.css" /><link rel="stylesheet" type="text/css" href="css/switch.css" /><link rel="stylesheet" type="text/css" href="css/menu.css" />');
</script>
</html>

</script><?php 
	include_once 'bootstrap.php';
	initpage();
	

	$func = function() {
		$xml = file_get_contents("dropdowns.xml");
		getxmlhtmlcselect($xml,$_GET,'pivot config','dpivot');
	};
	gethtmldiv("Main",$func,Array(),"containswitch","divlabel");
	
	$source_type = flip_source_type();
	
	//$args = array('comment'=>'this is a comment','divlabel' => 'this is a div label','label' => 'dsfdf');						
	
	$args = array('comment'=>'What instance of the datatype do you want to view;For instance id the datatype selected was student then Booker could be chosen; if datatype=adult had been chosen, then the list of available adults would be shown in the dropdown','divlabel' => 'View Config','label' => 'Datatype Value');							
	getchtmldbselect($SSDB,'lesson',$source_type,"source_value",1,$_GET['source_value'],$args);
						
	$func = function() {
		$args = array('checked'=>explode(",",$_GET['ztypes']),'comment' => 'Enables an alternative display that uses color to make it easier to see patterns across grids of data');	
		getchtmlswitch("formats","formats",$args);
		$args['comment'] = 'Rollup multiple entries where they only differ by student, to conserve space on the screen';	
		getchtmlswitch("rollup","rollup",$args); 
		$args['comment'] = 'Display the number of records in each cell instead of the records themselves';
		getchtmlswitch("count","count",$args); 
	};
	gethtmldiv("Visual Config",$func,Array(),"containswitch","divlabel");
	
	$func = function() {
		$args = array('checked'=>explode(",",$_GET['ztypes']),'comment' => 'Choose what datafields you want to see in a cell of the grid');	
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
	
	gethtmldiv("datafields",$func,Array(),"containswitch","divlabel");		
	
	$func = function($args) {
		$SSDB = $args[0];

		$comment = 'Filter the grid to only show rows that match this criteria';
		$args = array('comment'=>$comment, 'label' => 'Subject',"distinct" => false);							
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],$args);	
		$args = array('comment'=>$comment, 'label' => 'Weekday',"distinct" => false);			
		getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],$args);		
		$args = array('comment'=>$comment, 'label' => 'Period',"distinct" => false);					
		getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],$args);
		$args = array('comment'=>$comment, 'label' => 'Student',"distinct" => false);							
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],$args);
		$args = array('comment'=>$comment, 'label' => 'Teacher',"distinct" => false);			
		getchtmldbselect($SSDB,'lesson','adult',"cnstr_adult",1,$_GET['cnstr_adult'],$args);
		$args = array('comment'=>$comment, 'label' => 'Prep');				
		getchtmldbselect($SSDB,'lesson','prep',"cnstr_prep",1,$_GET['cnstr_prep'],$args);		
		$args = array('comment'=>$comment, 'label' => 'Source File');			
		getchtmldbselect($SSDB,'lesson','source',"cnstr_source",1,$_GET['cnstr_source'],$args);
		$args = array('comment'=>$comment, 'label' => 'Record Type','manualvalues' => Array('wp','ap','academic','seminar'));	
		getchtmldbselect($SSDB,'lesson','recordtype',"cnstr_recordtype",1,$_GET['cnstr_recordtype'],$args);
	};
	gethtmldiv("select filters",$func,Array($SSDB),"contain","divlabel");	

	
	$func = function($args) {
		$SSDB = $args[0];

		//getdbhtmlmultiselect($dbname,$query,$name,$maxy=0,$checked=NULL) {
		getdbhtmlmultiselect($SSDB,'select distinct name from dow','cnstr_dow',Array('checked' => $_GET,'maxy' => 10));
		getdbhtmlmultiselect($SSDB,'select distinct name from period','cnstr_period',Array('checked' => $_GET,'maxy' => 10));
	};
	gethtmldiv("select filters",$func,Array($SSDB),"wideswitch","divlabel");	
	
?>
		
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],
'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script></html>

<?php
	if(isset($_GET['ztypes'])) {
		$token =refreshpage();
		echo "<br><br>";
		
		$func = function() use ($token,$_GET) {
			$args = Array('noheader' => true,'id' => 'table2');
			draw($token,$_GET);
		};
		$title = "Pivot Table: ".$_GET['source_type']."=".$_GET['source_value'];
		gethtmldiv($title,$func,"table","divlabel");	
	}
?>

<script src="afterload.js"></script>
