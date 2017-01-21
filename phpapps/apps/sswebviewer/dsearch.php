<html>
<script src="jquery-3.1.1.js"></script>
<script src="stylesheets.js"></script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("dropdowns.xml");
	
	getxmlhtmlcselect($xml,$_GET,'label','dsearch');		
	
	$func = function() {
		global $SSDB;
		
		//,array("distinct" => false));
		//getchtmldbselect($SSDB,"lesson",$_item->valuetype,$valuetype,$widgetcount,$_item->value,array("distinct" => false));

 		//getchtmldbselect($dbname,$tablename,$column,$name,$widgetcount,$default,$args){
		getchtmldbselect($SSDB,'lesson','subject',"cnstr_subject",1,$_GET['cnstr_subject'],array("distinct" => false));
		getchtmldbselect($SSDB,'lesson','dow',"cnstr_dow",1,$_GET['cnstr_dow'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','period',"cnstr_period",1,$_GET['cnstr_period'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','student',"cnstr_student",1,$_GET['cnstr_student'],NULL,"comment");
		getchtmldbselect($SSDB,'lesson','teacher',"cnstr_adult",1,$_GET['cnstr_adult'],NULL,"comment");
	};
	gethtmldiv("select filters",$func,"contain","divlabel");	
	
	$func = function() {
		$args = array('checked'=>explode(",",$_GET['ztypes']),'comment' => 'Choose what datafields you want to see in a cell of the grid');	
		getchtmlswitch("status","status",$args);
		getchtmlswitch("subject","subject",$args);
		getchtmlswitch("adult","adult",$args);
		getchtmlswitch("student","student",$args);
		getchtmlswitch("record","record",$args);
		getchtmlswitch("recordtype","recordtype",$args);
		getchtmlswitch("id","id",$args);
	};
	
	gethtmldiv("datafields",$func,"containswitch","divlabel");		
?>

// need some js that will call schema when type is selected so can give field selection box

<!--<script src="dpivot.js"></script>-->
<script>
var ztypes = new Array();
var url = "";

function buildurl() {
 	url = "http://".concat(Globals.server_name,"/",Globals.script_name,"?");
   	
   	ztypes = new Array();
   		
   	$('select').each(function (index, value) {
	   		url = url + this.id + "=" + this.value + "&";
	   });
	    		
	  $('input').each(function (index, value) {    			
	  		if (this.checked == true) {
	  			ztypes.push(this.id);	
	  		}
	  		else {
	  			url = url + this.id + "=" + this.value + "&";
	  		}
	   });
    		
    	url = url + "ztypes=" + ztypes.join();
  return url
}

$(document).ready(function(){
   $("select, input").on('change',function(){
    	url = buildurl();
    	//console.log(url);
    	get(url);
   });
   
});

function get(url) {
	console.log(url);
	window.location = url;
}
</script>
<script src="stylesheets.js"></script>
<script>var Globals = <?php echo json_encode(array(
'script_name' => $_SERVER['PHP_SELF'],'server_name' => $_SERVER['SERVER_NAME'])); 
?>;</script>

<?php

$_GET['parser']="drawform";

if(isset($_GET['ztypes'])) {
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

?>