import sqlite3
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from xml_utils import get_xml_elements,get_xml_child_elements,get_xml_element

db_schema_file="./schema.xml"

tables = get_xml_elements(db_schema_file,".//Table")

for table in tables:
    print "table=",table.attrib
    idcolumn_name=get_xml_element(db_schema_file,".//IDColumn",table).text
    print "idcol=",idcolumn_name
    columns = get_xml_elements(db_schema_file,".//Column",table)
    for column in columns:
        print "col=",get_xml_child_elements(column)
exit()

sqlite_file = "food.sqlite"
table_food_des = "FOOD_DES"
column_ndbno = "NDB_No"
column_fdggrpcd = "FdGrp_Cd"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

c.execute('CREATE TABLE {table} ({column} {column_type})'\
          .format(table=table_food_des,
                 column=column_ndbno,
                 column_type='INTEGER'))

c.execute("ALTER TABLE {table} ADD COLUMN '{column}' {column_type}"\
          .format(table=table_food_des,
                 column=column_fdggrpcd,
                 column_type='TEXT'))

c.execute("INSERT INTO {table} ({idcolumn},{column})VALUES (1234,'test')"\
          .format(table=table_food_des,
                 idcolumn=column_ndbno,
                 column=column_fdggrpcd))


conn.commit()
conn.close()

