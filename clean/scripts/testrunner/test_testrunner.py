import unittest
from testrunner import testsuite_get, testsuite_run,testsuite_results
class Test_testrunner(unittest.TestCase):
    '''def test_testsuite_get(self):
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir')
        
        self.assertEqual(testsummary,expected_results)
        
        
    def test_testsuite_run(self):
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir')
        testsuite_run(suite)
        
        #self.assertEqual(testsummary,expected_results)
        
    def test_testsuite_results(self):
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir')
        testresult = testsuite_run(suite)
        
        testsuite_results(testresult)
        
        #self.assertEqual(testsummary,expected_results)'''
        
    def test_testsuite_results_failures(self):
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir_fail')
        testresult = testsuite_run(suite)
        
        testsuite_results(testresult)
        
    def test_testsuite_results_error(self):
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir_error')
        testresult = testsuite_run(suite)
        
        testsuite_results(testresult)
        
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_testrunner)
    unittest.TextTestRunner(verbosity=2).run(suite) 