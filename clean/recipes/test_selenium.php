<?php

set_include_path('/home/burtnolej/Development/pythonapps3/phpapps/utils/');
include_once 'ui_utils.php';


function draw($submitpage) {
?>

<html>
	<body>
		<?php echo "<form action='".$submitpage."' method='post' accept-charset='UTF-8'>";?>
	
			<fieldset >
				<input type='hidden' name='submitted' id='submitted' value='1'/>
				<div>
				<?php
				
					$xml = "<root>
									<dropdown id='1'>
										<field>xaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<default>dow</default>
									</dropdown>
									<dropdown id='2'>
										<field>yaxis</field>
										<values>
											<value>period</value>
											<value>dow</value>
											<value>adult</value>
											<value>subject</value>
										</values>
										<default>period</default>
									</dropdown>
									<dropdown id='3'>
										<field>source_type</field>
										<values>
											<value>student</value>
											<value>adult</value>
										</values>
										<default>student</default>
									</dropdown>
									<dropdown id='4'>
										<field>source_value</field>
										<values>
											<value>Peter</value>
										</values>
										<default>Peter</default>
									</dropdown>
								</root>";
					
					echo "<div id='one'>";

					gethtmlxmldropdown($xml);

					gethtmlbutton('submit','go');
					
				?>
				</div>
			</fieldset>
		</form>
	</body>
</html>
<?php
}

draw('foobar.php');
