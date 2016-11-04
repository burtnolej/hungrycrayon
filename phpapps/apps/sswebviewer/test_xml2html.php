<?php

require_once __DIR__ . '/composer/vendor/autoload.php';

include_once 'xml2html.php';
include_once '../../utils/utils_error.php';
include_once '../../utils/utils_utils.php';

include_once './testcases/testcases_xml2html.php';

set_error_handler('\\UtilsError::error_handler');

class Test_xml2html extends PHPUnit_Framework_TestCase
{
	public function test_1row1cell1value()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell>row1cell1</td></tr></table> ";
				
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>row1cell1</value>
									</cell>
								</row>
							</root>";
								
		$_result = drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_1row1cellformats()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell bgcolor=#66FF33 fgcolor=#251151>row1cell1</td></tr></table> ";
				
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>row1cell1</value>
										<fgcolor>251151</fgcolor>
										<bgcolor>66FF33</bgcolor>
									</cell>
								</row>
							</root>";
								
		$_result = drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	
	public function test_1row2cell1value()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell>row1cell1</td><td id=cell>row1cell2</td></tr></table> ";
				
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>row1cell1</value>
									</cell>
									<cell id = '1.2'>
										<value>row1cell2</value>
									</cell>
								</row>
							</root>";
								
		$_result = drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_2row2cell1value()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell>row1cell1</td><td id=cell>row1cell2</td></tr><tr><td id=cell>row2cell1</td><td id=cell>row2cell2</td></tr></table> ";
				
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>row1cell1</value>
									</cell>
									<cell id = '1.2'>
										<value>row1cell2</value>
									</cell>
								</row>
								<row id='2'>
									<cell id = '2.1'>
										<value>row2cell1</value>
									</cell>
									<cell id = '2.2'>
										<value>row2cell2</value>
									</cell>
								</row>
							</root>";
								
		$_result = drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_subcell()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td><table id=table><tr><td id=cell bgcolor=#33FFEF fgcolor=#251151>row1subcell1</td><td id=cell bgcolor=#7233FF fgcolor=#251151>row1subcell2</td></tr></table></td><td id=cell bgcolor=#FAFF33 fgcolor=#251151>row1cell2</td></tr></table> ";

		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<subcell id = '1.1.1'>
											<value>row1subcell1</value>
											<fgcolor>251151</fgcolor>
											<bgcolor>33FFEF</bgcolor>
										</subcell>
										<subcell id = '1.1.2'>
											<value>row1subcell2</value>
											<fgcolor>251151</fgcolor>
											<bgcolor>7233FF</bgcolor>
										</subcell>
									</cell>
									<cell id = '1.2'>
										<value>row1cell2</value>
										<fgcolor>251151</fgcolor>
										<bgcolor>FAFF33</bgcolor>
									</cell>
								</row>
							</root>";
								
		$_result = drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_header()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=rowhdrcell bgcolor=#FAFF33 fgcolor=#251151>row1cell1</td><td id=cell bgcolor=#66FF33 fgcolor=#251151>row2cell1</td></tr></table> ";
		$this->xmlstr= "
				<root>
					<row id='1'>
						<cell id = '1.1'>
							<type>rowhdrcell</type>
							<value>row1cell1</value>
							<fgcolor>251151</fgcolor>
							<bgcolor>FAFF33</bgcolor>
						</cell>
						<cell id = '2.1'>
							<value>row2cell1</value>
							<fgcolor>251151</fgcolor>
							<bgcolor>66FF33</bgcolor>
						</cell>
					</row>
				</root>";
				
		
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();
		$this->assertEquals($result,$this->expected_result);
	}
}

$st = new Test_xml2html();
$st->test_header();
$st->test_1row1cell1value();
$st->test_1row2cell1value();
$st->test_2row2cell1value();
$st->test_1row1cellformats();
$st->test_subcell();

?>
