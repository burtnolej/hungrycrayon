<?php

function gettablecolumns($dbname,$tablename){

	$columns = array();
	
	$db = new SQLite3($dbname);
	
	$results = $db->query("pragma table_info(".$tablename.")");
	
	while ($row = $results->fetchArray()) {
		if (substr($row[1],0,2) <> "__") {
			$columns[] = $row[1];
		}
	}
	
	return($columns);
}

function getcolumndistinctvalues($dbname,$tablename,$colname) {
		
	$values = array();
	
	$db = new SQLite3($dbname);
	
	$results = $db->query("select distinct(".$colname.") from ".$tablename);
	
	while ($row = $results->fetchArray()) {
		$values[] = $row[0];
	}
	
	return $values;
}

?>