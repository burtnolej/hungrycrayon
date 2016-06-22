<?php

class Mineral
{
    // property declaration
    private $var_name = Null;
    public $sources = Null;
    public $daily_requirement = Null;

    function __construct($var_name,$sources,$daily_requirement)
    {

        if (gettype($sources) != "array")
        {
            echo "Error";
        }

        $this->var_name = $var_name;
        $this->sources = $sources;
        $this->daily_requirement = $daily_requirement;
    }

    public function dump(){
        echo $this->var_name;

    }
}

/*class A
{
    function foo()
    {
        if (isset($this)) {
            echo '$this is defined (';
            echo get_class($this);
            echo ")\n";
        } else {
            echo "\$this is not defined.\n";
        }
    }
}

class B
{
    function bar()
    {
        // Note: the next line will issue a warning if E_STRICT is enabled.
        A::foo();
    }
}

$a = new A();
$a->foo();

// Note: the next line will issue a warning if E_STRICT is enabled.
A::foo();
$b = new B();
$b->bar();

// Note: the next line will issue a warning if E_STRICT is enabled.
B::bar();
?>
*/

$mnl = new Mineral("calcium",array("milk"=>"10mg/8oz"),15);

$mnl->dump();
?>