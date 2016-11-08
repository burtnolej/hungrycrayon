<?php

require_once __DIR__ . '/composer/vendor/autoload.php';

include_once 'xml2html.php';
include_once '../../utils/utils_error.php';
include_once '../../utils/utils_utils.php';

//include_once './testcases/testcases_xml2html.php';

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
										<fgcolor>#251151</fgcolor>
										<bgcolor>#66FF33</bgcolor>
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
											<fgcolor>#251151</fgcolor>
											<bgcolor>#33FFEF</bgcolor>
										</subcell>
										<subcell id = '1.1.2'>
											<value>row1subcell2</value>
											<fgcolor>#251151</fgcolor>
											<bgcolor>#7233FF</bgcolor>
										</subcell>
									</cell>
									<cell id = '1.2'>
										<value>row1cell2</value>
										<fgcolor>#251151</fgcolor>
										<bgcolor>#FAFF33</bgcolor>
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
							<fgcolor>#251151</fgcolor>
							<bgcolor>#FAFF33</bgcolor>
						</cell>
						<cell id = '2.1'>
							<value>row2cell1</value>
							<fgcolor>#251151</fgcolor>
							<bgcolor>#66FF33</bgcolor>
						</cell>
					</row>
				</root>";

		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();
		$this->assertEquals($result,$this->expected_result);
	}
	
}
class Test_xml2html_function extends PHPUnit_Framework_TestCase
{
	public function test_1row_1col_2subrow_1subcol()
	{
		//ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell bgcolor=#FFFFFF fgcolor=#000000></td><td id=cell bgcolor=#FFFFFF fgcolor=#000000>MO</td></tr><tr><td id=cell bgcolor=#FFFFFF fgcolor=#000000>830-910</td><td><table id=table><tr><td id=cell bgcolor=#ffcc99 fgcolor=#FFFFFF>ELA</td><td id=cell bgcolor=#99ffcc fgcolor=#FFFFFF>Math</td></tr></table></td></tr></table> ";
        
		$this->xmlstr= "
         <root>
          <row id='1'>
            <cell id='1.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id='1.2'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id='2'>
            <cell id='2.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id='2.2'>
              <subrow id='2.2.1'>
                <subcell id='2.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id='2.2.2'>
                <subcell id='2.2.2.1'>
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
              </subrow>
            </cell>
          </row>
        </root>";
        
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		//ob_end_clean();
		//$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_2row_1col_2subrow_1subcol()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell bgcolor=#ffffff fgcolor=#000000></td><td id=cell bgcolor=#ffffff fgcolor=#000000>MO</td></tr><tr><td id=cell bgcolor=#ffffff fgcolor=#000000>830-910</td><td><table id=table><tr><td id=cell bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td></tr><tr><td id=cell bgcolor=#99ffcc fgcolor=#ffffff>Math</td></tr></table></td></tr><tr><td id=cell bgcolor=#ffffff fgcolor=#000000>910-950</td><td><table id=table><tr><td id=cell bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td></tr><tr><td id=cell bgcolor=#99ffcc fgcolor=#ffffff>Math</td></tr></table></td></tr></table> ";
		
		$this->xmlstr= "
	        <root>
          <row id='1'>
            <cell id='1.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id='1.2'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id='2'>
            <cell id='2.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id='2.2'>
              <subrow id='2.2.1'>
                <subcell id='2.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id='2.2.2'>
                <subcell id='2.2.2.1'>
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
              </subrow>
            </cell>
          </row>
          <row id='3'>
            <cell id='3.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>910-950</value>
            </cell>
            <cell id='3.2'>
              <subrow id='3.2.1'>
                <subcell id='3.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id='3.2.2'>
                <subcell id='3.2.2.1'>
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
              </subrow>
            </cell>
          </row>
        </root>";
        
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_1row_1col_2subrow_2subcol()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = "<table id=table ><tr><td id=cell bgcolor=#ffffff fgcolor=#000000></td><td id=cell bgcolor=#ffffff fgcolor=#000000>MO</td></tr><tr><td id=cell bgcolor=#ffffff fgcolor=#000000>830-910</td><td><table id=table><tr><td id=cell bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td><td id=cell bgcolor=#006600 fgcolor=#00ff00>Amelia</td></tr><tr><td id=cell bgcolor=#99ffcc fgcolor=#ffffff>Math</td><td id=cell bgcolor=#d3d3d3 fgcolor=#ffffff>Aaron</td></tr></table></td></tr></table> ";
				
		$this->xmlstr= "	
		   <root>
          <row id='1'>
            <cell id='1.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id='1.2'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id='2'>
            <cell id='2.1'>
              <bgcolor>#ffffff</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell><cell id='2.2'>
              <subrow id='2.2.1'>
                <subcell id='2.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>ELA</value>
                </subcell>
                <subcell id='2.2.1.2'>
                  <bgcolor>#006600</bgcolor>
                  <fgcolor>#00ff00</fgcolor>
                  <value>Amelia</value>
                </subcell>
              </subrow>
              <subrow id='2.2.2'>
                <subcell id='2.2.2.1'>
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Math</value>
                </subcell>
                <subcell id='2.2.2.2'>
                  <bgcolor>#d3d3d3</bgcolor>
                  <fgcolor>#ffffff</fgcolor>
                  <value>Aaron</value>
                </subcell>
              </subrow>
            </cell>
          </row>
        </root>";
        
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();
		$this->assertEquals($result,$this->expected_result);
	}

	public function test_nrow_ncol_2subrow_1subcol()
	{
		//ob_start(); // buffer echos; so can use buffer in string compare of output
						
		$this->xmlstr= "<root><row id='1'><cell id='1.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id='1.2'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>??</value></cell><cell id='1.3'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Karolina</value></cell><cell id='1.4'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Paraic</value></cell><cell id='1.5'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Issey</value></cell><cell id='1.6'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>[Paraic,Rahul]</value></cell><cell id='1.7'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Amelia</value></cell></row><row id='2'><cell id='2.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id='2.2' /><cell id='2.3' /><cell id='2.4' /><cell id='2.5' /><cell id='2.6' /><cell id='2.7'><subrow id='2.7.1'><subcell id='2.7.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='2.7.1.2'><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row><row id='3'><cell id='3.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>910-950</value></cell><cell id='3.2'><subrow id='3.2.1'><subcell id='3.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='3.2.1.2'><bgcolor>#666600</bgcolor><fgcolor>#ffffff</fgcolor><value>Core</value></subcell></subrow></cell><cell id='3.3' /><cell id='3.4' /><cell id='3.5' /><cell id='3.6' /><cell id='3.7' /></row><row id='4'><cell id='4.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>950-1030</value></cell><cell id='4.2' /><cell id='4.3' /><cell id='4.4'><subrow id='4.4.1'><subcell id='4.4.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='4.4.1.2'><bgcolor>#006600</bgcolor><fgcolor>#ffffff</fgcolor><value>Science</value></subcell></subrow></cell><cell id='4.5' /><cell id='4.6' /><cell id='4.7' /></row><row id='5'><cell id='5.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1030-1110</value></cell><cell id='5.2' /><cell id='5.3' /><cell id='5.4' /><cell id='5.5'><subrow id='5.5.1'><subcell id='5.5.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='5.5.1.2'><bgcolor>#ff99cc</bgcolor><fgcolor>#ffffff</fgcolor><value>History</value></subcell></subrow></cell><cell id='5.6' /><cell id='5.7' /></row><row id='6'><cell id='6.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1110-1210</value></cell><cell id='6.2'><subrow id='6.2.1'><subcell id='6.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='6.2.1.2'><bgcolor>#663300</bgcolor><fgcolor>#ffffff</fgcolor><value>Computer Time</value></subcell></subrow></cell><cell id='6.3' /><cell id='6.4' /><cell id='6.5' /><cell id='6.6' /><cell id='6.7' /></row><row id='7'><cell id='7.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1210-100</value></cell><cell id='7.2' /><cell id='7.3' /><cell id='7.4' /><cell id='7.5' /><cell id='7.6'><subrow id='7.6.1'><subcell id='7.6.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='7.6.1.2'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>??</value></subcell></subrow></cell><cell id='7.7' /></row><row id='8'><cell id='8.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>100-140</value></cell><cell id='8.2' /><cell id='8.3' /><cell id='8.4' /><cell id='8.5' /><cell id='8.6' /><cell id='8.7'><subrow id='8.7.1'><subcell id='8.7.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='8.7.1.2'><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row><row id='9'><cell id='9.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>140-220</value></cell><cell id='9.2' /><cell id='9.3'><subrow id='9.3.1'><subcell id='9.3.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='9.3.1.2'><bgcolor>#ccff99</bgcolor><fgcolor>#ffffff</fgcolor><value>Counseling</value></subcell></subrow></cell><cell id='9.4' /><cell id='9.5' /><cell id='9.6' /><cell id='9.7' /></row><row id='10'><cell id='10.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>220-300</value></cell><cell id='10.2'><subrow id='10.2.1'><subcell id='10.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='10.2.1.2'><bgcolor>#ff99cc</bgcolor><fgcolor>#ffffff</fgcolor><value>Movement</value></subcell></subrow></cell><cell id='10.3' /><cell id='10.4' /><cell id='10.5' /><cell id='10.6' /><cell id='10.7' /></row><row id='11'><cell id='11.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>300-330</value></cell><cell id='11.2'><subrow id='11.2.1'><subcell id='11.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='11.2.1.2'><bgcolor>#663300</bgcolor><fgcolor>#ffffff</fgcolor><value>Computer Time</value></subcell></subrow></cell><cell id='11.3' /><cell id='11.4' /><cell id='11.5' /><cell id='11.6' /><cell id='11.7' /></row></root>";
		
		drawgrid($this->xmlstr);
		//$result = ob_get_contents();
		//ob_end_clean();
		//$this->assertEquals($result,$this->expected_result);
	}
}

$st = new Test_xml2html();

/*
$st->test_header();
$st->test_1row1cell1value();
$st->test_1row2cell1value();
$st->test_2row2cell1value();
$st->test_1row1cellformats();
$st->test_subcell();
*/
$stf = new Test_xml2html_function();

//$stf->test_1row_1col_2subrow_1subcol();
//$stf->test_2row_1col_2subrow_1subcol();
//$stf->test_1row_1col_2subrow_2subcol();
$stf->test_nrow_ncol_2subrow_1subcol();

?>
