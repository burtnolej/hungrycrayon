<?php
/**
 * Created by PhpStorm.
 * User: burtnolej
 * Date: 6/18/16
 * Time: 7:44 AM
 */

include "Workout.php";
?>

<form name="form" action="" method="get">
    <input type="text" name="duration" id="duration" value="blah">
    <input type="text" name="start_time" id="start_time" value="blah blah">
</form>

<?php

$iwout = new IntervalWorkout($_GET['duration'], $_GET['start_time']);

?>


