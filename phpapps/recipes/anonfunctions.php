

<?php

function execit($func) {
	$func();
}

function foo() {
	$a = array(1,2,3,4);
	for($i=0;$i<10;$i++) {
		$func = function () use ($a) {
			echo "blah";
			echo sizeof($a);
		};
		
		execit($func);
	}
	
	

}


foo();

?>