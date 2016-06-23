


<?php
require_once 'HTML/Table.php';

$data = array(
 '0' => array('Bakken', 'Stig', '', 'stig@example.com'),
 '1' => array('Merz', 'Alexander', 'alex.example.com', 'alex@example.com'),
 '2' => array('Daniel', 'Adam', '', '')
);

$attrs = array('width' => '600');
$table = new HTML_Table($attrs);
$table->setAutoGrow(true);
$table->setAutoFill('n/a');


for ($nr = 0; $nr < count($data); $nr++) {
  $table->setHeaderContents($nr+1, 0, (string)$nr);
  for ($i = 0; $i < 4; $i++) {
    if ('' != $data[$nr][$i]) {
      $table->setCellContents($nr+1, $i+1, $data[$nr][$i]);
    }
  }
}
$altRow = array('bgcolor' => 'red');
$table->altRowAttributes(1, null, $altRow);

$table->setHeaderContents(0, 0, '');
$table->setHeaderContents(0, 1, 'Surname');
$table->setHeaderContents(0, 2, 'Name');
$table->setHeaderContents(0, 3, 'Website');
$table->setHeaderContents(0, 4, 'EMail');
$hrAttrs = array('bgcolor' => 'silver');
$table->setRowAttributes(0, $hrAttrs, true);
$table->setColAttributes(0, $hrAttrs);

echo $table->toHtml();

?>