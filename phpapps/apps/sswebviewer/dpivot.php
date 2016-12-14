<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
<script src="stylesheets.js"></script>
</html>

</script><?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("dropdowns.xml");
	getxmlhtmlcselect($xml,$_GET,'pivot config','dpivot');
	
	$source_type = flip_source_type();
	
	//$args = array('comment'=>'this is a comment','divlabel' => 'this is a div label','label' => 'dsfdf');						
	
	$args = array('comment'=>'What instance of the datatype do you want to view;For instance id the datatype selected was student then Booker could be chosen; if datatype=adult had been chosen, then the list of available adults would be shown in the dropdown','divlabel' => 'View Config','label' => 'Datatype Value');							
	getchtmldbselect($SSDB,'lesson',$source_type,"source_value",1,$_GET['source_value'],$args);
						
	$func = function() {
		$args = array('checked'=>explode(",",$_GET['ztypes']),'comment' => 'Enables an alternative display that uses color to make it easier to see patterns across grids of data');	
		getchtmlswitch("formats","formats",$args);
		$args['comment'] = 'Rollup multiple entries where they only differ by student, to conserve space on the screen';	
		getchtmlswitch("rollup","rollup",$args); 
	};
	gethtmldiv("Visual Config",$func,"containswitch","divlabel");
	
	$func = function() {
		$args = array('checked'=>explode(",",$_GET['ztypes']),'comment' => 'Choose what datafields you want to see in a cell of the grid');	
		getchtmlswitch("status","status",$args);
		getchtmlswitch("subject","subject",$args);
		getchtmlswitch("adult","adult",$args);
		getchtmlswitch("student","student",$args);
	};
	
	gethtmldiv("datafields",$func,"containswitch","divlabel");		
	
	$func = function() {
		global $SSDB;

		$comment = 'Filter the grid to only show rows that match this criteria';
		$args = array('comment'=>$comment, 'label' => 'Subject');							
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],$args);		
		$args = array('comment'=>$comment, 'label' => 'Weekday');			
		getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],$args);		
		$args = array('comment'=>$comment, 'label' => 'Period');			
		getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],$args);
		$args = array('comment'=>$comment, 'label' => 'Student');					
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],$args);
		$args = array('comment'=>$comment, 'label' => 'Teacher');	
		getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],$args);
		$args = array('comment'=>$comment, 'label' => 'Prep');	
		getchtmldbselect($SSDB,'lesson','prep',"cnstr_prep",1,$_GET['cnstr_prep'],$args);
	};
	gethtmldiv("select filters",$func,"contain","divlabel");	
?>

<script src="dpivot.js"></script>
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],
'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script></html>

<?php
	if(isset($_GET['ztypes'])) {
		$token =refreshpage();
		echo "<br><br>";
		
		$func = function() use ($token,$args) {
			draw($token,$args);
		};
		
		gethtmldiv("select filters",$func,"table","divlabel");	
	}
?>