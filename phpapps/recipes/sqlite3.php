



<?php
$db = new SQLite3('test.sqlite');

$results = $db->query('SELECT * FROM lesson');
while ($row = $results->fetchArray()) {
    var_dump($row);
}
?>

