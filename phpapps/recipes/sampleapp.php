<?php

class LogFile
{

	public $filename = Null;
	public $fh = Null;

	function __construct($filename)
	{
		$this->fh = fopen($filename,"w") or die("could not open file");
	}

	function __destruct()
	{
		fclose($this->fh);
	}
}
		
		
class BaseClass
{
	function __construct()
	{
		echo __FUNCTION__;
	}
}

class HTMLTableBuilder
{
	function __construct($gridarray)
	{
		echo "<table border='1' style=width:100%>";

		foreach ($gridarray as $rowarray) {
			$this->htmlrow($rowarray);
		}
		echo "</table> ";
	}

	function htmlcell($content)
	{
		echo "<td bgcolor='#FF0000'>";
		echo $content;
		echo "</td>";
	}
	function htmlrow($rowarray,$headerflag)
	{
		if (gettype($rowarray) != "array")
		{
			echo "Error";
		}
		else
		{
			if ($headerflag == True) {
				echo "<th>";
			}
			else {
				echo "<tr>";
			}
			foreach ($rowarray as $content)
			{
				$this->htmlcell($content);
			}
			if ($headerflag == True) {
				echo "</th>";
			}
			else {
				echo "</tr>";
			}
		}
	}
}

class MultiDArray extends BaseClass
{
	public $arr = Null;
	function __construct($maxrows,$maxcols)
	{
		$this->arr = array();
		if (gettype($maxrows) != "integer")
		{
			echo "Error";
		}

		for ($i = 0; $i < $maxrows; $i++) {
			$rowarr = array();
			for ($j = 0; $j < $maxcols; $j++) {
				$colarr = array();
				array_push($rowarr,$i.$j);
			}
			array_push($this->arr,$rowarr);
		}
	}

	function dump()
	{
		foreach ($this->arr as $rowarr) 
		{
			foreach ($rowarr as $content) 
			{
				print $content;
			}
			print PHP_EOL;
		}
	}
}

$mdarray = new MultiDArray(10,10);
//$mdarray->dump();

$testarray = [ [1,2],[3,4],];
$htmltbl = new HTMLTableBuilder($mdarray->arr);
$logfile = new LogFile("foobar.txt");

fwrite($logfile->fh,"foobar")

?>
