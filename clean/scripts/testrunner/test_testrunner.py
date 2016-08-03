import unittest
from testrunner import testsuite_get, testsuite_run,testsuite_results
class Test_testrunner(unittest.TestCase):
    def test_testsuite_get(self):
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22'] }
        suite, testsummary = testsuite_get('./dir')
        
        self.assertEqual(testsummary,expected_results)
        
    def test_testsuite_run(self):
        # allow dupe has to be set as the prev test may not have released the module
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir',allowdupe=True)
        testsuite_run(suite)
        
        self.assertEqual(testsummary,expected_results)
        
    def test_testsuite_results(self):
        # allow dupe has to be set as the prev test may not have released the module
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir',allowdupe=True)
        testresult = testsuite_run(suite)
        
        testsuite_results(testresult)
        
        self.assertEqual(testsummary,expected_results)
        
    def test_testsuite_results_failures(self):
        
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir_fail')
        testresult = testsuite_results(testsuite_run(suite))
        self.assertEquals(testresult['#failures'],2)
        
    def test_testsuite_results_error(self):
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir_error',allowdupe=True)
        testresult = testsuite_results(testsuite_run(suite))
        self.assertEquals(testresult['#errors'],2)
    
class Test_testrunner2(unittest.TestCase):
    def test_ignore(self):
        expected_results = {'test_test1.py': ['Test_Test', 'Test_Test2'], 'test_test2.py': ['Test_Test21', 'Test_Test22']}
        suite, testsummary = testsuite_get('./dir_error',allowdupe=True,ignoredir=['./dir_error/subdir'])
        testresult = testsuite_results(testsuite_run(suite))
        self.assertEquals(testresult['#errors'],1)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_testrunner)
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_testrunner2))
    unittest.TextTestRunner(verbosity=2).run(suite) 