<map version="0.9.0">
    <node TEXT="Database:diet"><node TEXT="Table:food"><node TEXT="Column:name"><node TEXT="DBType:text" />
                <node TEXT="nullable:true" />
            </node>
            <node TEXT="Column:calories"><node TEXT="DBType:integer" />
		<node TEXT="nullable:true" />
            </node>
	</node>
	<node TEXT="Table:meals"><node TEXT="Column:type"><node TEXT="DBType:text" />
		<node TEXT="nullable:true" />
	    </node>
	    <node TEXT="Column:time"><node TEXT="DBType:datetime" />
		<node TEXT="nullable:true" />
	    </node>
        </node>
    </node>
    <node TEXT="Database:fitness"><node TEXT="Table:workout"><node TEXT="Key:date" />
            <node TEXT="Column:date"><node TEXT="DBType:datetime" />
                <node TEXT="nullable:true" />
            </node>
            <node TEXT="Column:type"><node TEXT="DBType:text" />
		<node TEXT="nullable:true" />
            </node>
	</node>
	<node TEXT="Row:"><node TEXT="Table:workout" />
	    <node TEXT="Column:date"><node TEXT="Key:date" />
	        <node TEXT="Value:250772" />
	    </node>
	    <node TEXT="Column:type"><node TEXT="Value:&quot;cycling&quot;" />
	    </node>
	</node>
	<node TEXT="Row:"><node TEXT="Table:workout" />
	    <node TEXT="Column:date"><node TEXT="Value:260772" />
	    </node>
	    <node TEXT="Column:type"><node TEXT="Value:&quot;rowing&quot;" />
	    </node>
	</node>
    </node>
</map>
