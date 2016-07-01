<?php

$xmlstr = <<<XML
<menu>
	<label>root</label>
	<item>
		<tag>buildingconfiguring</tag>
		<label>Building and Configuring</label>
		<source>build-install.php</source>
		<item>
			<tag>php</tag>
			<label>PHP</label>
			<source>build-install.php</source>
			<item>
				<tag>phpdependencies</tag>
				<label>PHP Dependencies</label>
			</item>
			<item>
				<tag>configurephp</tag>
				<label>Configure PHP</label>
			</item>
			<item>
				<tag>troubleshootingphp</tag>
				<label>Troubleshooting PHP</label>
			</item>
			<item>
				<tag>buildphp</tag>
				<label>Build PHP</label>
			</item>
			<item>
				<tag>testphp</tag>
				<label>Testing PHP</label>
			</item>
		</item>
		<item>
			<tag>apache</tag>
			<label>Apache</label>
			<source>build-install.php</source>
			<item>
				<tag>httpdvapache</tag>
				<label>HTTPD vs Apache2</label>
			</item>
			<item>
				<tag>firewallconfig</tag>
				<label>Firewall Config</label>
			</item>
			<item>
				<tag>linkedinmodules</tag>
				<label>Linked in Modules</label>
			</item>
			<item>
				<tag>makingsureitworks</tag>
				<label>Making sure it works</label>
			</item>
			<item>
				<tag>troubleshooting</tag>
				<label>Troubleshooting</label>
			</item>
			<item>
				<tag>proxyserver</tag>
				<label>Proxy Server</label>
			</item>
			<item>
				<tag>logverbosity</tag>
				<label>Log Verbosity</label>
			</item>
		</item>
		<item>
			<label>Bluefish</label>
			<tag>bluefish</tag>
			<source>build-install.php</source>
		</item>
		<item>
			<tag>phpdebugger</tag>
			<label>PHP Debugger (php)</label>
			<source>build-install.php</source>
			<item>
				<tag>buildingphpdbg</tag>
				<label>Building phpdbg</label>
			</item>
			<item>
				<tag>Usingphpdbg</tag>
				<label>Using phpdbg</label>
			</item>
		</item>
	</item>
	<item>
		<label>Libraries Modules</label>
		<source>libraries-modules.php</source>
		<item>
			<label>Apache</label>
			<item>
				<tag>apr</tag>
				<label>Apache Portable Runtime (apr,aprlib)</label>
			</item>
			<item>
				<tag>modphp</tag>
				<label>mod-php</label>
			</item>
		</item>
		<item>
			<label>PHP</label>
			<item>
				<tag>mysql</tag>
				<label>MySQL</label>
			</item>
			<item>
				<tag>apxs</tag>
				<label>apxs</label>
			</item>
		</item>
		<item>
			<label>Misc.</label>
			<item>
				<tag>libxml</tag>
				<label>libxml</label>
			</item>
			<item >
				<tag>readline</tag>
				<label>readline</label>
			</item>
			<item>
				<tag>mysql</tag>
				<label>MySql</label>
			</item>
			<item>
				<tag>buildessentials</tag>
				<label>Build Essentials</label>
			</item>
			<item>
				<tag>pcre</tag>
				<label>Perl Compatible RegEx (pcre)</label>
			</item>
			<item>
				<tag>zlib</tag>
				<label>zlib</label>
			</item>
		</item>
	</item>
	<item>
		<label>OS</label>
		<item >
			<label>xwin</label>
			<tag>xwin</tag>
		</item>
		<item>
			<label>xprop</label>
			<tag>xprop</tag>
		</item>
		<item>
			<label>kde</label>
			<tag>kde</tag>
			<items>
				<item>
					<label>kdeconfig</label>
					<tag>kdeconfig</tag>
				</item>
				<item>
					<label>kdeautostart</label>
					<tag>kdeautostart</tag>
				</item>
			</items>
		</item>
		<item>
			<label>Packaging Tools</label>
			<tag>packagingtools</tag>
		</item>
		<item>
			<label>Packaging Tools</label>
			<tag>packagingtools</tag>
			<item>
				<label>apt</label>
				<tag>apt</tag>
			</item>
			<item>
				<label>dpkg</label>
				<tag>dpkg</tag>
			</item>
			<item>
				<label>pkg-config</label>
				<tag>pkg-config</tag>
			</item>
			<item>
				<label>configure</label>
				<tag>configure</tag>
			</item>				
		</item>
	</item>
	<item>
		<source>html-html.php</source>
		<label>HTML</label>
		<tag>false</tag>
		<item>
			<tag>httpdconf</tag>
			<label>httpdconf</label>
		</item>
		<item>
			<tag>htmllists</tag>
			<label>htmllists</label>
		</item>
		<item>
			<tag>htmltable</tag>
			<label>htmltable</label>
		</item>
		<item>
			<tag>htmllinks</tag>
			<label>htmllinks</label>
		</item>
		<item>
			<tag>htmlescaping</tag>
			<label>htmlescaping</label>
		</item>
	</item>
	<item>
		<label>Web Frameworks</label>
		<item>
			<label>WordPress</label>
			<item>
				<tag>wpsetup</tag>
				<label>Setup</label>
			</item>
		</item>
	</item>
	<item >
		<label>UNIX Tools</label>
		<item>
			<label>Shared Libraries</label>
			<item>
				<tag>ldconfig</tag>
				<label>ldconfig</label>
			</item>
		</item>
	</item>
	<item>
		<label>Config</label>
		<item>
			<label>php.ini</label>
			<tag>php.ini</tag>
		</item>
		<item>
			<label>httpdconf</label>
			<tag>phttpdconf</tag>
		</item>
	</item>
</menu>
XML;
?>