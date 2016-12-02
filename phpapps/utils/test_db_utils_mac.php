<?php


	function test_()
	{
		$dbname = "test_gettablerows.sqlite";
		$tablename = "lesson";
	
		$db = new SQLite3($dbname);
		
		$columns = $db->query("pragma table_info(".$tablename.")");
		
	   while ($row = $columns->fetchArray()) {
		 	if (substr($row[1],0,2) <> "__") {
				$results[] = $row[1];
			}
		}
	
		print_r($results);
		
		$results = $db->query("select * from ".$tablename);
	
		$row1 = $results->fetchArray();
	
		foreach ($results as $field) {
		
			$values[] = $field[1];
			
			print($field." ".$row1[$field].PHP_EOL);
			//foreach ($rows as $row) {
			//	print_r($row);
			//
			}
			print_r($values);
		}

	
test_();


?>
