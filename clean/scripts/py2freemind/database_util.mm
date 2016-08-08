<map version="0.9.0">
	<node TEXT="database_util.xml"><node TEXT="Database"><node TEXT="execute"><node TEXT="self"><node TEXT="Name:self" /></node>
			<node TEXT="sql_str"><node TEXT="Name:sql_str" /></node>
			<node TEXT="singleval"><node TEXT="Name:singleval" /></node>
			<node TEXT="False"><node TEXT="Name:False" /></node>
			<node TEXT="defexecute(self,sql_str,singleval"><node TEXT="Name:defexecute(self,sql_str,singleval" /></node>
			<node TEXT="ifsingleval"><node TEXT="Name:ifsingleval" /></node>
			<node TEXT="sql_result"><node TEXT="Name:sql_result" /></node>
			<node TEXT="sql_result"><node TEXT="Name:sql_result" /></node>
		<node TEXT="Name:execute" /></node>
		<node TEXT="description"><node TEXT="self"><node TEXT="Name:self" /></node>
		<node TEXT="Name:description" /></node>
		<node TEXT="tbl_get"><node TEXT="self"><node TEXT="Name:self" /></node>
			<node TEXT="sql_result"><node TEXT="Name:sql_result" /></node>
			<node TEXT="self.tbl"><node TEXT="Name:self.tbl" /></node>
			<node TEXT="_d"><node TEXT="Name:_d" /></node>
			<node TEXT="_d[db_enum.s3_tbl_attrib[i]]"><node TEXT="Name:_d[db_enum.s3_tbl_attrib[i]]" /></node>
			<node TEXT="self.tbl[_d[&quot;name&quot;]]"><node TEXT="Name:self.tbl[_d[&quot;name&quot;]]" /></node>
		<node TEXT="Name:tbl_get" /></node>
		<node TEXT="remove"><node TEXT="self"><node TEXT="Name:self" /></node>
		<node TEXT="Name:remove" /></node>
		<node TEXT="tbl_exists"><node TEXT="self"><node TEXT="Name:self" /></node>
			<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
		<node TEXT="Name:tbl_exists" /></node>
		<node TEXT="open"><node TEXT="self"><node TEXT="Name:self" /></node>
			<node TEXT="self.connection"><node TEXT="Name:self.connection" /></node>
			<node TEXT="self.cursor"><node TEXT="Name:self.cursor" /></node>
		<node TEXT="Name:open" /></node>
	<node TEXT="Name:Database" /></node>
	<node TEXT="col_type_enum"><node TEXT="Name:col_type_enum" /></node>
	<node TEXT="db_enum"><node TEXT="Name:db_enum" /></node>
	<node TEXT="schema_col_get"><node TEXT="schema"><node TEXT="Name:schema" /></node>
		<node TEXT="name"><node TEXT="Name:name" /></node>
		<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
	<node TEXT="Name:schema_col_get" /></node>
	<node TEXT="schema_data_get"><node TEXT="schema_file"><node TEXT="Name:schema_file" /></node>
		<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
		<node TEXT="xml"><node TEXT="Name:xml" /></node>
		<node TEXT="child_xml"><node TEXT="Name:child_xml" /></node>
		<node TEXT="rows"><node TEXT="Name:rows" /></node>
		<node TEXT="ifrow_xml.attrib['Table']"><node TEXT="Name:ifrow_xml.attrib['Table']" /></node>
		<node TEXT="tbl_col_name"><node TEXT="Name:tbl_col_name" /></node>
		<node TEXT="tbl_rows"><node TEXT="Name:tbl_rows" /></node>
	<node TEXT="Name:schema_data_get" /></node>
	<node TEXT="schema_execute"><node TEXT="schema_file"><node TEXT="Name:schema_file" /></node>
		<node TEXT="config"><node TEXT="Name:config" /></node>
		<node TEXT="database"><node TEXT="Name:database" /></node>
		<node TEXT="tbl_col_defn,tbl_pk_defn,_"><node TEXT="Name:tbl_col_defn,tbl_pk_defn,_" /></node>
	<node TEXT="Name:schema_execute" /></node>
	<node TEXT="schema_get"><node TEXT="schema"><node TEXT="Name:schema" /></node>
	<node TEXT="Name:schema_get" /></node>
	<node TEXT="schema_print"><node TEXT="schema"><node TEXT="Name:schema" /></node>
	<node TEXT="Name:schema_print" /></node>
	<node TEXT="schema_read"><node TEXT="schema_file"><node TEXT="Name:schema_file" /></node>
		<node TEXT="name_enum"><node TEXT="Name:name_enum" /></node>
		<node TEXT="type_enum"><node TEXT="Name:type_enum" /></node>
		<node TEXT="xml"><node TEXT="Name:xml" /></node>
		<node TEXT="child_xml"><node TEXT="Name:child_xml" /></node>
		<node TEXT="config"><node TEXT="Name:config" /></node>
		<node TEXT="_names"><node TEXT="Name:_names" /></node>
		<node TEXT="tbl_config"><node TEXT="Name:tbl_config" /></node>
		<node TEXT="_tbl_names"><node TEXT="Name:_tbl_names" /></node>
		<node TEXT="tbl_pk_defn"><node TEXT="Name:tbl_pk_defn" /></node>
		<node TEXT="tbl_pk_defn"><node TEXT="Name:tbl_pk_defn" /></node>
		<node TEXT="tbl_col_defn"><node TEXT="Name:tbl_col_defn" /></node>
		<node TEXT="tbl_config[tbl_name]"><node TEXT="Name:tbl_config[tbl_name]" /></node>
	<node TEXT="Name:schema_read" /></node>
	<node TEXT="schema_tbl_get"><node TEXT="schema"><node TEXT="Name:schema" /></node>
		<node TEXT="name"><node TEXT="Name:name" /></node>
	<node TEXT="Name:schema_tbl_get" /></node>
	<node TEXT="schema_tbl_pk_get"><node TEXT="schema"><node TEXT="Name:schema" /></node>
		<node TEXT="name"><node TEXT="Name:name" /></node>
		<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
	<node TEXT="Name:schema_tbl_pk_get" /></node>
	<node TEXT="sqlite3"><node TEXT="Name:sqlite3" /></node>
	<node TEXT="sys"><node TEXT="Name:sys" /></node>
	<node TEXT="tbl_create"><node TEXT="database"><node TEXT="Name:database" /></node>
		<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
		<node TEXT="col_defn"><node TEXT="Name:col_defn" /></node>
		<node TEXT="tbl_pk_defn"><node TEXT="Name:tbl_pk_defn" /></node>
		<node TEXT="deftbl_create(database,tbl_name,col_defn,tbl_pk_defn"><node TEXT="Name:deftbl_create(database,tbl_name,col_defn,tbl_pk_defn" /></node>
		<node TEXT="sql_col_str"><node TEXT="Name:sql_col_str" /></node>
		<node TEXT="sql_str"><node TEXT="Name:sql_str" /></node>
		<node TEXT="sql_col_str"><node TEXT="Name:sql_col_str" /></node>
		<node TEXT="sql_pk_str"><node TEXT="Name:sql_pk_str" /></node>
		<node TEXT="sql_str"><node TEXT="Name:sql_str" /></node>
		<node TEXT="sql_result"><node TEXT="Name:sql_result" /></node>
	<node TEXT="Name:tbl_create" /></node>
	<node TEXT="tbl_index_count"><node TEXT="database"><node TEXT="Name:database" /></node>
		<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
		<node TEXT="sql_str"><node TEXT="Name:sql_str" /></node>
		<node TEXT="sql_str+"><node TEXT="Name:sql_str+" /></node>
		<node TEXT="sql_result"><node TEXT="Name:sql_result" /></node>
	<node TEXT="Name:tbl_index_count" /></node>
	<node TEXT="tbl_index_defn_get"><node TEXT="database"><node TEXT="Name:database" /></node>
		<node TEXT="tbl_name"><node TEXT="Name:tbl_name" /></node>
		<node TEXT="sql_str"><node TEXT="Name:sql_str" /></node>
		<node TEXT="sql_result"><node TEXT="Name:sql_result" /></node>
	<node TEXT="Name:tbl_index_defn_get" /></node>
</node></map>