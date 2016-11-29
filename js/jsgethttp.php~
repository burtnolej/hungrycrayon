<!DOCTYPE html>
<?php
function draw_login() {
?>
	
<html>
	<body>
		<form>
			<select id="mySelect" name="mySelect"  onchange="get()"> 
				<option value="">Please select</option>
				<option value="Adelia">Adelia</option>
				<option value="Donny">Donny</option>
			</select>
			
				
			<input id="myCheck" type=checkbox  value="c1" onchange="get()">blah</input>
		</form>
		<p id="demo"></p>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js">

		function get() {
    		var s = document.getElementById("mySelect").value;
    		
    		var c = document.getElementById("myCheck").checked;
    
	    	window.location = "http://192.168.1.154/jsgethttp.php/student/"+s+"?foo="+c;
		}

		function reqListener () {
  			console.log(this.responseText);
		}
		</script>
	</body>
</html>
<?php
}

draw_login();

if(isset($_GET['foo'])) {
	echo $_GET['foo'];
	//$args = $_POST;
	//$SSRESTURL = getenv("SSRESTURL");
	//$url = buildurl($SSRESTURL,$args);
	//$token = getcurl($url);
	//draw($token,$args);
}

?>
