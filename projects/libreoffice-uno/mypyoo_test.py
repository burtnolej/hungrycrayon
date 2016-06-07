# -*- coding: UTF-8 -*-
"""
PyOO - Pythonic interface to Apache OpenOffice API (UNO)

Copyright (c) 2016 Seznam.cz, a.s.

"""

import contextlib
import datetime
import unittest

import pyoo


desktop = None

def setUpModule():
    global desktop
    desktop = pyoo.Desktop()

@pyoo.str_repr
class MyObject(object):
    def __str__(self):
        return u'my object'

class BaseDocumentTestCase(unittest.TestCase):
    """
    Base class for test cases which require a new spreadsheet document.
    """

    @classmethod
    def setUpClass(cls):
        cls.document = desktop.create_spreadsheet()

    @classmethod
    def tearDownClass(cls):
        cls.document.close()
    
class BaseOpenDocumentTestCase(unittest.TestCase):
    """
    Base class for test cases which require an existing spreadsheet document.
    """

    @classmethod
    def setUpClass(cls):
        cls.document = desktop.open_spreadsheet("/home/burtnolej/Development/pythonapps3/projects/libreoffice-uno/uno_test.ods")

    @classmethod
    def tearDownClass(cls):
        cls.document.close()
        
class CellRangeTestCase(BaseDocumentTestCase):

    def setUp(self):
        self.sheet = self.document.sheets[0]

    def test_cell_data(self):
        self.sheet[10,1].value = 300
        
        self.assertEqual(300, self.sheet[10,1].value)
    
class CellRangeExistingSpreadsheet(BaseOpenDocumentTestCase):
    def setUp(self):
        self.sheet = self.document.sheets[0]
        
    def test_cell_data(self):
        self.assertEqual(600, self.sheet[20,1].value)    

    def test_get_maxrange_from_sheet(self):
        
        cells = self.sheet[:,:] # whole sheet               
        self.assertEqual('$A$1:$AMJ$1048576', str(cells.address)) # just output the address
        
    def test_get_range_from_sheet(self):

        cells = self.sheet[20:30,10:14]                
        self.assertEqual('$K$21:$N$30', str(cells.address))
        
    def test_get_values_from_range(self):

        results = (('A','B','C'),('D','E','F'),('G','H','I'))
        
        # in both cases (row,col) the end value needs to be one more than expected
        # so we would expect $K$5:$M$7 to be 4:6,10,12 when its actually as below
        cells = self.sheet[4:7,10:13] # $K$5:$M$7
        self.assertEqual(results, cells.values)
       
    def test_get_values_from_vartical_range(self):
        
        results = ('A','D','G')
        cells = self.sheet[4:7,10:13]
        column = cells[:,0]
        
        self.assertEqual(results, column.values)
        
class QueryRangeExistingSpreadsheet(BaseOpenDocumentTestCase):
    def setUp(self):
        self.sheet = self.document.sheets[0]
        
    def test_get_values_from_range(self):
        
        # range defn ($K$5:$M$7)
        # in both cases (row,col) the end value needs to be one more than expected
        # so we would expect $K$5:$M$7 to be 4:6,10,12 when its actually as below        
        y_start=19
        y_end=33
        x_start=10
        x_end=15

        expected_results = {'database':"test.sqlite",'table':"XYZ",
                            'columns':4,'rows':9,'field':"id,A,B,C"}
        
        dbmeta_enum = ['database','table','columns','rows','field']
        
        # extract the row headers (column #1)
        cells = self.sheet[y_start:y_end,x_start:x_end] 
        row_headers = cells[:len(dbmeta_enum),1]
        
        _d = {}
        for _dbmeta in dbmeta_enum:
            _id = dbmeta_enum.index(_dbmeta)            
            _d[_dbmeta] = row_headers[_id].value
            
        self.assertEqual(expected_results, _d) 
        
        # ranges for the data table (ie removing the meta data)
        # these will be the rows to be inserted to the db
        datarow_y_start = len(dbmeta_enum)
        datarow_y_end = y_end - y_start
        datacol_x_start = 1
        datacol_x_end = x_end - x_start + 1

        datatable = cells[datarow_y_start:datarow_y_end,
                          datacol_x_start:datacol_x_end]
        
        #datatable = cells[datarow_y_start:datarow_y_end,
        #                  :]
        
        print(datatable)
        print(datatable.values)
        expected_results = (("A1",1,2,3),
                            ("A2",4,5,6),
                            ("A3",7,8,9),
                            ("A4",10,11,12),
                            ("A5",13,14,15),
                            ("A6",16,17,18),
                            ("A7",19,20,21),
                            ("A8",22,23,24),
                            ("A9",25,26,27))    
        
        
        print(expected_results)
        
        self.assertEqual(expected_results, datatable.values) 
        
if __name__ == '__main__':
    unittest.main()
