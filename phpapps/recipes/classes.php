<?php

class BaseClass
{
	function __construct()
	{
		// prints out the current function name
		echo __FUNCTION__;
	}
}

class Mineral extends BaseClass
{
	private $var_name = Null;
	public $sources = Null;
	public $daily_requirement = Null;
	
	function __construct($var_name,$sources,$daily_requirement)
	{
		parent::__construct();
			 	
		if (gettype($sources) != "array")
		{
			echo "Error";
		}
	
	$this->var_name = $var_name;
	$this->sources = $sources;
	$this->daily_requirement = $daily_requirement;
	}

	public function dump()
	{
		echo $this->var_name;
	}
}


		print_r(get_class_methods($item));
		
				//method_exists($item;
		
		

function print_power($base,$exp)
{
	printf("\n%d to the power %d = %d\n",$base,$exp,pow($base,$exp));
}

//print_power(12,4);

call_user_func("print_power",12,4);
	
//$mnl = new Mineral("calcium",array("milk"=>"10mg/8oz"),15);
//$mnl->dump();
?>