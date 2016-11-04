<?php

$xmlstr = <<<XML
<root>
	<row id='1'>
		<cell id = '1.1'>
			<value>row1cell1</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>FAFF33</bgcolor>
		</cell>
	</row>
	<row id='2'>
		<cell id = '2.1'>
			<value>row2cell1</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>66FF33</bgcolor>
		</cell>
	</row>
	<row id='3'>
		<cell id = '3.1'>
			<subcell id = '3.1.1'>
				<value>row3subcell1</value>
				<fgcolor>251151</fgcolor>
				<bgcolor>33FFEF</bgcolor>
			</subcell>
			<subcell id = '3.1.2'>
				<value>row3subcell2</value>
				<fgcolor>251151</fgcolor>
				<bgcolor>7233FF</bgcolor>
			</subcell>
		</cell>
	</row>

</root>
XML;

$xmlstrlarge = <<<XML
<root>
	<row id='1'>
		<cell id = '1.1'>
			<value>row1cell1</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>FAFF33</bgcolor>
		</cell>
		<cell id = '1.2'>
			<value>row1cell2</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>FAFF33</bgcolor>
		</cell>
	</row>
	<row id='2'>
		<cell id = '2.1'>
			<value>row2cell1</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>66FF33</bgcolor>
		</cell>
		<cell id = '2.2'>
			<value>row2cell2</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>66FF33</bgcolor>
		</cell>
	</row>
	<row id='3'>
		<cell id = '3.1'>
			<subcell id = '3.1.1'>
				<value>row3subcell1</value>
				<fgcolor>251151</fgcolor>
				<bgcolor>33FFEF</bgcolor>
			</subcell>
			<subcell id = '3.1.2'>
				<value>row3subcell2</value>
				<fgcolor>251151</fgcolor>
				<bgcolor>7233FF</bgcolor>
			</subcell>
		</cell>
		<cell id = '3.2'>
			<value>row3cell2</value>
			<fgcolor>251151</fgcolor>
			<bgcolor>66FF33</bgcolor>
		</cell>
	</row>

</root>
XML;


?>