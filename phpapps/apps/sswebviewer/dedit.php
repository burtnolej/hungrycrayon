<html>
<!--<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>-->
<script  type="text/javascript"  src="jquery-3.1.1.js"></script>
<script src="stylesheets.js"></script>
<script  type="text/javascript"  src="document_utils.js"></script>
</html>

<?php 
	include_once 'bootstrap.php';
	initpage();
	
	$xml = file_get_contents("inputs.xml");
	gethtmlbutton("button","submit");
	getxmlhtmlinput($xml,$_GET,'div label',"dedit");
	
?>

<script src="dedit.js"></script>
<script src="stylesheets.js"></script>
<script src="document_utils.js"></script>

<script>

var Globals = <?php echo json_encode(array(
		'script_name' => $_SERVER['PHP_SELF'],
		'server_name' => $_SERVER['SERVER_NAME'],
 		'watch_list' => array("source_value"))); ?>;

function isarray(obj) {
  /* returns true if the passed object is an array */
  if (Object.prototype.toString.call(obj) === '[object Array]') {
    return true;
  }
  return false;
}
function compare_1darrays(arr1, arr2) {
  /* both arguments must be 1d arrays; returns 0 if identical or 
		returns an array with the indexes of the elements that are different
		in it */
  if (!isarray(arr1) || !isarray(arr2)) {
    throw ('both arguments need to be of type array')
  } 
  else if (arr1.length != arr2.length) {
    throw ('arrays are different lengths')
  } 
  else {
    var diffs = Array();
    for (i = 0; i < arr1.length; i++) {
      if (arr1[i] != arr2[i]) {
        diffs.push(i);
      }
    }
    if (diffs.length != 0) {
      return diffs
    }
  }
  return 0
}

function getElementValues(type) {
	var values = Array();
	$(type).each(function (index, value) {
   		values.push(this.value);
	});
	return values;
}

function getElementValueChanges(elementtype,initvalues) {
	newvalues = getElementValues(elementtype);
	diffvalues = compare_1darrays(initvalues,newvalues);
	ids = getElementsIds(elementtype);
	result = Array();

	for (i=0;i<diffvalues.length;i++) {
		result.push(ids[diffvalues[i]]);
		result.push(newvalues[diffvalues[i]]);
	}
	
	return result;
}

function getElementsIds(type) {
	var values = Array();
	$(type).each(function (index, id) {
   		values.push(this.id);
	});
	return values;
}

var ztypes = new Array();
var url = "";

$(document).ready(function(){
	
	var initvalues = getElementValues("select");
	var results = Array();
			
	// first check if this is event is a submit button press
	$("input[name='button']").on('click',function(){
		
		url = buildurl();
		url = url + "&page_status=submit";
		
		// add the changes to 
		results = getElementValueChanges("select",initvalues);
		url = url + "&value_changes="+results.join(",");
		console.log(url);
		get(url);
	});
		
	$("select, input").on('change',function(){
		// if the element that changed is on the watchlist redraw the page
		if (Globals.watch_list.indexOf(this.id)  != -1) {
			url = buildurl();
 			get(url);
		}
 	});
});





</script>

<?php

if(isset($_GET['page_status'])) {
	$_GET['source_type']="update";
	//$_GET['source_value']="lesson";
	//$_GET['source_value']="id";
	$token =refreshpage();
	$_GET['parser']="drawform";
	echo "<br>update me<br>";
	//draw($token,$args);
}

if(isset($_GET['source_value'])) {
	$_GET['source_type']="id";
$_GET['parser']="drawform";
	$token =refreshpage();
	echo "<br><br>";
	draw($token,$args);
}

?>