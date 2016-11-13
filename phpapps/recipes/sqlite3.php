



<?php
$db = new SQLite3('test.sqlite');

//$results = $db->query('SELECT * FROM lesson');
//while ($row = $results->fetchArray()) {
//    var_dump($row);
//}

$results = $db->query('SELECT prep FROM lesson');
while ($row = $results->fetchArray()) {
    echo $row['prep'].PHP_EOL;
}

?>

