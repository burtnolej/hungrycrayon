

abstract class run_switch_on_off extends base_run_switch
{
    const on-off = "--on-off";
}

abstract class run_switch_key_val
{
    const key-val = "--key-val";
}

abstract class run_switch_key_list
{
    const key-list = "--key-list";
}

function __usage() {
	echo "usage : --all-tests | --test <testname>".PHP_EOL;
}


function test_foobar() {
}
// Test 1 ------------------------------------------------------------

$test_name = 'test --list-tests on own';

assert_arrays_equal(array('--list-tests'=>null),
						 __clean_argv(array('--list-tests'=>null)),
						 $bool_result,$result_str);
						 
output_results($bool_result,$result_str,$test_name);

// Test 2 ------------------------------------------------------------
$test_name = 'test --list-tests - 1 test - no other test';

assert_arrays_equal(array('--list-tests'=>null,'--test-name'=>'foobar'),
						 __clean_argv(array('--list-tests'=>null,'--test-name'=>'foobar')),
						 $bool_result,$result_str);
						 
output_results($bool_result,$result_str,$test_name);


figure out if should pass straight list into __clean_argv as this will mirror sys.argv


// Test 3 ------------------------------------------------------------
$test_name = 'test --list-tests - 3 tests';

assert_arrays_equal(array('--list-tests'=>null,'--test-name'=>array('foobar','foobar2','foobar3')),
						 __clean_argv(array('--list-tests'=>null,'--test-name'=>'foobar',)),
						 $bool_result,$result_str);
						 
output_results($bool_result,$result_str,$test_name);