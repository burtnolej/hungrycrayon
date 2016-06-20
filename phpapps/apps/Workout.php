<?php

/**
 * Created by PhpStorm.
 * User: burtnolej
 * Date: 6/18/16
 * Time: 7:14 AM
 */
class Workout
{
    var $duration;
    var $start_time;
    var $samples;

    function Workout($duration,$start_time)
    {
        $this->duration = $duration;
        $this->start_time = $start_time;
    }

    function printme(

        $class_vars = get_class_vars($this);

        foreach ($class_vars as $name => $value) {
            echo "$name : $value\n";
}

    )
    {}
} // end of class Workout


// extend the base class
class IntervalWorkout extends Workout {

    var $num; // number of intervals in the workout
    var $interval_duration;
    var $rest_duration;
    var $start_watts;
    var $end_watts;
    var $duration;
    var $start_time;

    function IntervalWorkout($num,$interval_duration,$start_watts,$end_watts,
                             $start_time,$duration)
    {
        $this->Workout($duration,$start_time);
        $this->num = $num;
        $this->interval_duration = $interval_duration;
        $this->start_watts = $start_watts;
        $this->end_watts = $end_watts;
    }
} // end of class IntervalWorkout

?>