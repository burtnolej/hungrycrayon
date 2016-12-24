<html>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>

<script src="dtest.js"></script>

<script type="text/javascript">

$(document).ready(function(){

	console.log(window.location.search.substr(0))
	
	if (window.localStorage['visited2'] == null) {
		console.log("firstvisit");
		window.localStorage.setItem('visited2',true);
		loadit("http://192.168.1.154/dtest.php?empty=True");
	}
	else {
		console.log("visited");
	}
	
	

});

</script>

<?php
echo $_GET['empty'];

if(isset($_GET['empty'])) {
	//$token =refreshpage();
	echo "fgdfgfgdfggdfgf";
	//draw($token,$args);
}

?>

</html>