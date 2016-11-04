<?php

include_once '../utils/utils_xml.php';
include_once '../utils/utils_error.php';

class RESTComms
{
	private $curl = Null;
	public $url = Null;
	
	function __construct($url) {
		$email = 'burtnolejusa@gmail.com';
		$pass = 'g0ldm@n1';
		$data = base64_encode('email='.$email.'&password='.$pass);
	
		//$url='https://simple-note.appspot.com/api/login';
		//$url='localhost:8080/x';
		
		$this->url = $url;
		$this->curl = curl_init($this->url);

		//curl_setopt($this->curl, CURLOPT_POST,true);
		curl_setopt($this->curl, CURLOPT_VERBOSE,1);
		//curl_setopt($this->curl, CURLOPT_POSTFIELDS,$data);
		curl_setopt($this->curl, CURLOPT_RETURNTRANSFER,true);
		curl_setopt($this->curl, CURLOPT_HTTPHEADER, array("User-Agent: Test"));
		curl_setopt($this->curl, CURLOPT_HEADER,false);
	}

	function exec() {
		$token = curl_exec($this->curl);
		$http_status = curl_getinfo($this->curl, CURLINFO_HTTP_CODE);
		$stats = curl_getinfo($this->curl);


		// display xml as html		
		xml2html($token);
	}
	
	function __destruct() {
		
		curl_close($this->curl);
	}
}

function xml2html($xmlstr)
{
	// load xml string into XML Utils
	$utilsxml = simplexml_load_string($xmlstr, 'utils_xml');		

	// get a list of all rows
	$_rows = $utilsxml->xpath("//row");

	echo "<table border='1' style=width:100%>";

	foreach ($_rows as $_row) {
	
		echo "<tr>";
	
		// get a list of the cells (children) of this row
		$_cells = $_row->xpath("child::*");
	
		foreach ($_cells as $_cell) {

			echo "<td";
			echo " bgcolor=#".$_cell->bgcolor;
			echo " fgcolor=#".$_cell->fgcolor;
			echo ">";
			echo $_cell->value;
			echo "</td>";
		}
		echo "</tr>";
	}
	
	echo "</table> ";	
}

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

set_error_handler('\\UtilsError::error_handler');

//$mdarray = new MultiDArray(10,10);
//$mdarray->dump();

//$testarray = [ [1,2],[3,4],];
//$htmltbl = new HTMLTableBuilder($mdarray->arr);
//$logfile = new LogFile("foobar.txt");

//fwrite($logfile->fh,"foobar")

$restcomms = new RESTComms("localhost:8080/x");
$restcomms->exec();
=======
$mdarray = new MultiDArray(10,10);
//$mdarray->dump();

$testarray = [ [1,2],[3,4],];
$htmltbl = new HTMLTableBuilder($mdarray->arr);
$logfile = new LogFile("foobar.txt");

fwrite($logfile->fh,"foobar")

?>
