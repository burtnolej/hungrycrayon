<?php

/*
This works - the namespace PHPUnit_Framework_TestCase seems to work after 
we have recreated autoload from composer.

to run tests - phpunit unittest.php
*/
require_once __DIR__ . '/composer/vendor/autoload.php';

class StackTest extends PHPUnit_Framework_TestCase
{
    public function testPushAndPop()
    {
        $stack = [];
        $this->assertEquals(0, count($stack));

        array_push($stack, 'foo');
        $this->assertEquals('fox', $stack[count($stack)-1]);
        $this->assertEquals(1, count($stack));

        $this->assertEquals('foo', array_pop($stack));
    }
}

$st = new StackTest();

?>
