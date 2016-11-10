
<html>
<style>
label {
	display: inline-block;
	width:70px;
	text-alight=right;
}
</style>
</html>

<?php


function get_htmldbmultiselect($dbname,$query) {
	
		echo "<div class=\"container\">	";
		echo "<div style=\"width: 12em; float: bottom;\">";
		
		$db = new SQLite3($dbname);

		$results = $db->query($query);
		while ($row = $results->fetchArray()) {
				echo "<input id=\"".$row['name']."\" type=\"checkbox\" name=\"ingredients[]\" value=\"".$row['name']."\"/>";
				echo "<label for=\"".$row['name']."\">".$row['name']."</label>";
		}
		echo "</datalist>";
		echo "</div>";
}
get_htmldbmultiselect("test.sqlite","select name from sqlite_master;");

?>

