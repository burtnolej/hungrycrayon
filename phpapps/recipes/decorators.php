<?php

function decorate($func, $wrap)
{
    $orig = $wrap . '_' . $func;
    runkit_function_rename($func, $orig);
    
    $body = sprintf(
        "return call_user_func_array('%s', array_merge([ '%s' ], [ func_get_args() ]));",
        $wrap, $orig
    );
    
    
    //echo "rename function ",$func," as ",$orig,"\n";
    
    //$array_merge = array_merge([ $orig ], [ func_get_args() ]);
    //$body = sprintf("return call_user_func_array('%s', %s);", $wrap, $array_merge);
    
    //echo "create function ",$func."\n";
    //echo "with body ",$body."\n";

    runkit_function_add($func, '', $body);
}

function hello($name)
{
    echo "Hello, $name!\n";
}

function logger($func, $args)
{
    $name = explode('_', $func); // last function invoked.
    echo end($name) . '(' . implode(', ' , $args) . ")\n";
    return call_user_func_array($func, $args);
}

function timer($func, $args)
{
    $start = microtime(true);
    $result = call_user_func_array($func, $args);
    echo sprintf("%s: %f\n", $func, microtime(true) - $start);
    return $result;
}

decorate('hello', 'timer');
//decorate('hello', 'logger');

echo hello('Bob');

?>