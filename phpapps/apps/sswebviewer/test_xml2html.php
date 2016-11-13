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
		
		$this->expected_result ='<table id=table ><tr><td class="cell">r1c1</td></tr></table> ';
						
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>r1c1</value>
									</cell>
								</row>
							</root>";
		drawgrid($this->xmlstr);
		
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_1row1cellformats()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#66FF33 fgcolor=#251151>r1c1</td></tr></table> ';
						
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>r1c1</value>
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
	
	public function test_1row2cell1value()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell">r1c1</td><td class="cell">r1c2</td></tr></table> ';
						
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>r1c1</value>
									</cell>
									<cell id = '1.2'>
										<value>r1c2</value>
									</cell>
								</row>
							</root>";
								
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_2row2cell1value()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell">r1c1</td><td class="cell">r1c2</td></tr><tr><td class="cell">r2c1</td><td class="cell">r2c2</td></tr></table> ';
						
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<value>r1c1</value>
									</cell>
									<cell id = '1.2'>
										<value>r1c2</value>
									</cell>
								</row>
								<row id='2'>
									<cell id = '2.1'>
										<value>r2c1</value>
									</cell>
									<cell id = '2.2'>
										<value>r2c2</value>
									</cell>
								</row>
							</root>";
								
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_subcell()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td><table id=table><tr><td class="cell sub left" bgcolor=#33FFEF fgcolor=#251151>r1sc1</td><td class="cell sub right" bgcolor=#7233FF fgcolor=#251151>r1sc2</td></tr></table></td><td class="cell" bgcolor=#FAFF33 fgcolor=#251151>r1c2</td></tr></table> ';
		
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<subcell id = '1.1.1'>
											<value>r1sc1</value>
											<fgcolor>#251151</fgcolor>
											<bgcolor>#33FFEF</bgcolor>
										</subcell>
										<subcell id = '1.1.2'>
											<value>r1sc2</value>
											<fgcolor>#251151</fgcolor>
											<bgcolor>#7233FF</bgcolor>
										</subcell>
									</cell>
									<cell id = '1.2'>
										<value>r1c2</value>
										<fgcolor>#251151</fgcolor>
										<bgcolor>#FAFF33</bgcolor>
									</cell>
								</row>
							</root>";
								
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();		
		$this->assertEquals($result,$this->expected_result);
	}
	
	public function test_header()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell rowhdr" bgcolor=#FAFF33 fgcolor=#251151>r1c1</td><td class="cell" bgcolor=#66FF33 fgcolor=#251151>r2c1</td></tr></table> ';
		$this->xmlstr= "
				<root>
					<row id='1'>
						<cell id = '1.1'>
							<type>rowhdr</type>
							<value>r1c1</value>
							<fgcolor>#251151</fgcolor>
							<bgcolor>#FAFF33</bgcolor>
						</cell>
						<cell id = '2.1'>
							<value>r2c1</value>
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
	public function test_1row_1col_1subrow_1subcol()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#FFFFFF fgcolor=#000000></td><td class="cell" bgcolor=#FFFFFF fgcolor=#000000>MO</td></tr><tr><td class="cell" bgcolor=#FFFFFF fgcolor=#000000>830-910</td><td><table id=table><tr><td class="cell sub left" bgcolor=#ffcc99 fgcolor=#FFFFFF>ELA</td></tr></table></td></tr></table> ';
		
		$this->xmlstr= "
         <root>
          <row id='1'>
            <cell id='1.1'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id='1.2'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id='2'>
            <cell id='2.1'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id='2.2'>
              <subrow id='2.2.1'>
                <subcell id='2.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#FFFFFF</fgcolor>
                  <valuetype>subject</valuetype>
                  <value>ELA</value>
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
	
	public function test_1row_1col_1subrow_3subcol()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#FFFFFF fgcolor=#000000></td><td class="cell" bgcolor=#FFFFFF fgcolor=#000000>MO</td></tr><tr><td class="cell" bgcolor=#FFFFFF fgcolor=#000000>830-910</td><td><table id=table><tr><td class="cell sub left" bgcolor=#ffcc99 fgcolor=#FFFFFF>left</td><td class="cell sub middle" bgcolor=#ffcc99 fgcolor=#FFFFFF>middle</td><td class="cell sub right" bgcolor=#ffcc99 fgcolor=#FFFFFF>right</td></tr></table></td></tr></table> ';
				        
		$this->xmlstr= "
         <root>
          <row id='1'>
            <cell id='1.1'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id='1.2'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id='2'>
            <cell id='2.1'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id='2.2'>
              <subrow id='2.2.1'>
                <subcell id='2.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#FFFFFF</fgcolor>
                  <value>left</value>
                </subcell>
                <subcell id='2.2.1.2'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#FFFFFF</fgcolor>
                  <value>middle</value>
                </subcell>
                <subcell id='2.2.1.3'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#FFFFFF</fgcolor>
                  <value>right</value>
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
	
	public function test_1row_1col_2subrow_1subcol()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#FFFFFF fgcolor=#000000></td><td class="cell" bgcolor=#FFFFFF fgcolor=#000000>MO</td></tr><tr><td class="cell" bgcolor=#FFFFFF fgcolor=#000000>830-910</td><td><table id=table><tr><td class="cell sub left" bgcolor=#ffcc99 fgcolor=#FFFFFF>ELA</td></tr><tr><td class="cell sub left" bgcolor=#99ffcc fgcolor=#FFFFFF>Math</td></tr></table></td></tr></table> ';
		        
		$this->xmlstr= "
         <root>
          <row id='1'>
            <cell id='1.1'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value />
            </cell>
            <cell id='1.2'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>MO</value>
            </cell>
          </row>
          <row id='2'>
            <cell id='2.1'>
              <bgcolor>#FFFFFF</bgcolor>
              <fgcolor>#000000</fgcolor>
              <value>830-910</value>
            </cell>
            <cell id='2.2'>
              <subrow id='2.2.1'>
                <subcell id='2.2.1.1'>
                  <bgcolor>#ffcc99</bgcolor>
                  <fgcolor>#FFFFFF</fgcolor>
                  <value>ELA</value>
                </subcell>
              </subrow>
              <subrow id='2.2.2'>
                <subcell id='2.2.2.1'>
                  <bgcolor>#99ffcc</bgcolor>
                  <fgcolor>#FFFFFF</fgcolor>
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
	
	public function test_2row_1col_2subrow_1subcol()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000></td><td class="cell" bgcolor=#ffffff fgcolor=#000000>MO</td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>830-910</td><td><table id=table><tr><td class="cell sub left" bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td></tr><tr><td class="cell sub left" bgcolor=#99ffcc fgcolor=#ffffff>Math</td></tr></table></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>910-950</td><td><table id=table><tr><td class="cell sub left" bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td></tr><tr><td class="cell sub left" bgcolor=#99ffcc fgcolor=#ffffff>Math</td></tr></table></td></tr></table> ';
				
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
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000></td><td class="cell" bgcolor=#ffffff fgcolor=#000000>MO</td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>830-910</td><td><table id=table><tr><td class="cell sub left" bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td><td class="cell sub right" bgcolor=#006600 fgcolor=#00ff00>Amelia</td></tr><tr><td class="cell sub left" bgcolor=#99ffcc fgcolor=#ffffff>Math</td><td class="cell sub right" bgcolor=#d3d3d3 fgcolor=#ffffff>Aaron</td></tr></table></td></tr></table> ';
						
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
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result = '<table id=table ><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000></td><td class="cell" bgcolor=#ffffff fgcolor=#000000>??</td><td class="cell" bgcolor=#ffffff fgcolor=#000000>Karolina</td><td class="cell" bgcolor=#ffffff fgcolor=#000000>Paraic</td><td class="cell" bgcolor=#ffffff fgcolor=#000000>Issey</td><td class="cell" bgcolor=#ffffff fgcolor=#000000>[Paraic,Rahul]</td><td class="cell" bgcolor=#ffffff fgcolor=#000000>Amelia</td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>830-910</td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td></tr></table></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>910-950</td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#666600 fgcolor=#ffffff>Core</td></tr></table></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>950-1030</td><td class="cell"></td><td class="cell"></td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#006600 fgcolor=#ffffff>Science</td></tr></table></td><td class="cell"></td><td class="cell"></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>1030-1110</td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#ff99cc fgcolor=#ffffff>History</td></tr></table></td><td class="cell"></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>1110-1210</td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#663300 fgcolor=#ffffff>Computer Time</td></tr></table></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>1210-100</td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#d3d3d3 fgcolor=#ffffff>??</td></tr></table></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>100-140</td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#ffcc99 fgcolor=#ffffff>ELA</td></tr></table></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>140-220</td><td class="cell"></td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#ccff99 fgcolor=#ffffff>Counseling</td></tr></table></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>220-300</td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#ff99cc fgcolor=#ffffff>Movement</td></tr></table></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td></tr><tr><td class="cell" bgcolor=#ffffff fgcolor=#000000>300-330</td><td><table id=table><tr><td class="cell sub left" bgcolor=#d3d3d3 fgcolor=#ffffff>Peter</td><td class="cell sub right" bgcolor=#663300 fgcolor=#ffffff>Computer Time</td></tr></table></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td><td class="cell"></td></tr></table> ';
		$this->xmlstr= "<root><row id='1'><cell id='1.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value /></cell><cell id='1.2'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>??</value></cell><cell id='1.3'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Karolina</value></cell><cell id='1.4'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Paraic</value></cell><cell id='1.5'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Issey</value></cell><cell id='1.6'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>[Paraic,Rahul]</value></cell><cell id='1.7'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>Amelia</value></cell></row><row id='2'><cell id='2.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>830-910</value></cell><cell id='2.2' /><cell id='2.3' /><cell id='2.4' /><cell id='2.5' /><cell id='2.6' /><cell id='2.7'><subrow id='2.7.1'><subcell id='2.7.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='2.7.1.2'><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row><row id='3'><cell id='3.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>910-950</value></cell><cell id='3.2'><subrow id='3.2.1'><subcell id='3.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='3.2.1.2'><bgcolor>#666600</bgcolor><fgcolor>#ffffff</fgcolor><value>Core</value></subcell></subrow></cell><cell id='3.3' /><cell id='3.4' /><cell id='3.5' /><cell id='3.6' /><cell id='3.7' /></row><row id='4'><cell id='4.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>950-1030</value></cell><cell id='4.2' /><cell id='4.3' /><cell id='4.4'><subrow id='4.4.1'><subcell id='4.4.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='4.4.1.2'><bgcolor>#006600</bgcolor><fgcolor>#ffffff</fgcolor><value>Science</value></subcell></subrow></cell><cell id='4.5' /><cell id='4.6' /><cell id='4.7' /></row><row id='5'><cell id='5.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1030-1110</value></cell><cell id='5.2' /><cell id='5.3' /><cell id='5.4' /><cell id='5.5'><subrow id='5.5.1'><subcell id='5.5.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='5.5.1.2'><bgcolor>#ff99cc</bgcolor><fgcolor>#ffffff</fgcolor><value>History</value></subcell></subrow></cell><cell id='5.6' /><cell id='5.7' /></row><row id='6'><cell id='6.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1110-1210</value></cell><cell id='6.2'><subrow id='6.2.1'><subcell id='6.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='6.2.1.2'><bgcolor>#663300</bgcolor><fgcolor>#ffffff</fgcolor><value>Computer Time</value></subcell></subrow></cell><cell id='6.3' /><cell id='6.4' /><cell id='6.5' /><cell id='6.6' /><cell id='6.7' /></row><row id='7'><cell id='7.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>1210-100</value></cell><cell id='7.2' /><cell id='7.3' /><cell id='7.4' /><cell id='7.5' /><cell id='7.6'><subrow id='7.6.1'><subcell id='7.6.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='7.6.1.2'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>??</value></subcell></subrow></cell><cell id='7.7' /></row><row id='8'><cell id='8.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>100-140</value></cell><cell id='8.2' /><cell id='8.3' /><cell id='8.4' /><cell id='8.5' /><cell id='8.6' /><cell id='8.7'><subrow id='8.7.1'><subcell id='8.7.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='8.7.1.2'><bgcolor>#ffcc99</bgcolor><fgcolor>#ffffff</fgcolor><value>ELA</value></subcell></subrow></cell></row><row id='9'><cell id='9.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>140-220</value></cell><cell id='9.2' /><cell id='9.3'><subrow id='9.3.1'><subcell id='9.3.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='9.3.1.2'><bgcolor>#ccff99</bgcolor><fgcolor>#ffffff</fgcolor><value>Counseling</value></subcell></subrow></cell><cell id='9.4' /><cell id='9.5' /><cell id='9.6' /><cell id='9.7' /></row><row id='10'><cell id='10.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>220-300</value></cell><cell id='10.2'><subrow id='10.2.1'><subcell id='10.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='10.2.1.2'><bgcolor>#ff99cc</bgcolor><fgcolor>#ffffff</fgcolor><value>Movement</value></subcell></subrow></cell><cell id='10.3' /><cell id='10.4' /><cell id='10.5' /><cell id='10.6' /><cell id='10.7' /></row><row id='11'><cell id='11.1'><bgcolor>#ffffff</bgcolor><fgcolor>#000000</fgcolor><value>300-330</value></cell><cell id='11.2'><subrow id='11.2.1'><subcell id='11.2.1.1'><bgcolor>#d3d3d3</bgcolor><fgcolor>#ffffff</fgcolor><value>Peter</value></subcell><subcell id='11.2.1.2'><bgcolor>#663300</bgcolor><fgcolor>#ffffff</fgcolor><value>Computer Time</value></subcell></subrow></cell><cell id='11.3' /><cell id='11.4' /><cell id='11.5' /><cell id='11.6' /><cell id='11.7' /></row></root>";
		
		drawgrid($this->xmlstr);
		$result = ob_get_contents();
		ob_end_clean();
		$this->assertEquals($result,$this->expected_result);
	}
}

class Test_xml2html_extra extends PHPUnit_Framework_TestCase
{
	public function test_shrinkfont()
	{
		ob_start(); // buffer echos; so can use buffer in string compare of output
		
		$this->expected_result ='<table id=table ><tr><td class="cell" style="font-size: 55%;">12345678910</td></tr></table> ';
								
		$this->xmlstr = "<root>
								<row id='1'>
									<cell id = '1.1'>
										<shrinkfont>5</shrinkfont>
										<value>12345678910</value>
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
$st->test_1row1cell1value();
$st->test_1row1cellformats();
$st->test_1row2cell1value();
$st->test_2row2cell1value();
$st->test_subcell();
$st->test_header();

$stf = new Test_xml2html_function();
$stf->test_1row_1col_1subrow_1subcol();
$stf->test_1row_1col_1subrow_3subcol();
$stf->test_1row_1col_2subrow_1subcol();
$stf->test_2row_1col_2subrow_1subcol();
$stf->test_1row_1col_2subrow_2subcol();
$stf->test_nrow_ncol_2subrow_1subcol();

$stf = new Test_xml2html_extra();
$stf->test_shrinkfont();

/*
$stf = new Test_xml2html_function();
*/

?>
