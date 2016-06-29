<?php
$xmlstr = <<<XML
<top id="1">
	<label>thetop</label>
	<uppermiddle id="1.1">
		<label>theuppermiddle</label>
		<lowermiddle id="1.1.1">
			<label>thelowermiddle</label>
			<bottom id="1.1.1.1">
				<label>thebottom</label>
			</bottom>
		</lowermiddle>
		<lowermiddle id="1.1.2">
			<label>thelowermiddle</label>
			<bottom id="1.1.2.1">
				<label>thebottom</label>
			</bottom>
		</lowermiddle>
	</uppermiddle>
	<uppermiddle id="1.2">
		<label>theuppermiddle</label>
		<lowermiddle id="1.2.1">
			<label>thelowermiddle</label>
			<bottom id="1.2.1.1">
				<label>thebottom</label>
			</bottom>
		</lowermiddle>
		<lowermiddle id="1.2.2">
			<label>thelowermiddle</label>
			<bottom id="1.2.2.1">
				<label>thebottom</label>
			</bottom>
		</lowermiddle>
	</uppermiddle>
</top>
XML;
?>
