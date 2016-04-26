
import unittest


                          
class DBXMLAccessor(XMLParser):
    
    ''' 
    Provides convenient access to information parsed from an xml schema containing database definitons and contents
    ----------------------------------------------------------------------------------------------------------------
    
    2 return forms of methods:
    a) returns a list of strings (ie the names of the databases in the schema
    b) returns a list of xml Element objects (ie the XML trees containing databases in the schema)
    
    4 forms of calling each method:
    a) predicated by_element; accepts a root note (xml.etree object) as an arg and searches below their
    b) predicated by_element_content); accepts a tag value = Database="test_db1" 
    c) predicated by_tag
    c) predicated by_tag_attribute
    
    c) no predicate and returns all snippets/names that match criteria
    '''    
    
    def __init__(schema):
        self.schema = schema
    
    #
    # Databases
    #
    
    # no predicate; return the xml_snippets containing the details for a database
    def get_xml_databases_from_schema():
        databases = get_xml_elements(schema,".//Database")
    
    # predicated by name; return the xml_snippets containing the details for a database
    def get_xml_databases_from_schema(database_name):
        databases = get_tag_values(schema,".//Database",database_name)
        
    # no predicate: returns the actual names (strings) of the databases
    def get_database_names_from_schema():
        databases = get_xml_elements(schema,".//Database")

    #
    # Tables
    #
    
    def get_xml_tables_from_schema_by_name(database_name):
        return(get_xml_elements(self.schema,".//Table"),database)

    def get_xml_tables_from_schema_by_element(database_name):
        return(get_xml_elements(self.schema,".//Table"),database)
    
    def get_table_columns_from_schema(schema, table_name):
        pass
    
    def get_table_index_from_schema(schema, table_name):
        pass
    
    def get_table_datarows_from_schema(schema, table_name):
        pass
    
    def get_column_attr_from_schema(schema, table_name, column_name):
        pass    
    
    
class TestDBXMLParser(unittest.TestCase):
    
    def setUp():
        self.dbxmlparser = DBXMLParser("test_schema.xml")
        
    def test_get_xml_tables_from_schema_iter():
    
        xml_databases = self.dbxmlparser.get_databases_from_schema()
        self.assertEquals(len(xml_databases),2)
        
        self.assertEquals(xml_databases)
        
        
    if __name__ == "__main__":
        suite = unittest.TestLoader().loadTestsFromTestCase(TestXMLParser)
        unittest.TextTestRunner(verbosity=2).run(suite)
        