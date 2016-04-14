"Simple parser for Garmin TCX files."

from lxml import objectify
import unittest
from list_utils import list_append
from misc_utils import write_text_to_file, read_delim_text_from_file


from types import IntType,StringType, FloatType
' should use TcxInt here not the types'

__version__ = '0.1'
    

class TcxParser:
    
    lap_fields = ["Calories"]

    trackpoint_fields = ["Time","DistanceMeters","Cadence"]

    trackpoint_value_fields = ["HeartRateBpm"]

    extension_fields = ["Watts","Speed"]

    all_fields = trackpoint_fields + trackpoint_value_fields + extension_fields
    
    dump_filename = "/tmp/tmp.csv"
    
    trackpoints = []
    
    def __init__(self, tcx_file):
        tree = objectify.parse(tcx_file)
        self.root = tree.getroot()
        self.laps = self.root.Activities.Activity.Lap
        self.extract_trackpoints_xml()

    def get_laps(self):
        
        for lap in self.laps:
            for lap_field in self.lap_fields:  
                print getattr(lap,lap_field),
            print

    def get_num_laps(self):
        return len(self.laps)

    def get_total_calories(self):
        return sum(lap.Calories for lap in self.laps)

    def get_total_lap_time(self):
        return sum(lap.TotalTimeSeconds for lap in self.laps)

    def get_total_trackpoint_distance(self):
        distance=0
        
        for lap in self.laps:
            for track in lap.Track:
                for trackpoint in track.Trackpoint:
                    distance = distance + trackpoint.DistanceMeters
        
        return distance
    
    def dump_to_csv(self):
        
        output = ""
        for record in self.records:
            for el in record:
                print type(el.text)
                output = output + ",".join(record)
            
        #write_text_to_file(self.dump_filename,output)
    
    
    def get_field_val_by_name(self,record_id,field_name):
        ' for 1 record'
        return(self.records[record_id][TcxParser.all_fields.index(field_name)])
    
    def get_field_sumval_by_name(self,field_name):
        ' for multiple records'
        return sum(record[TcxParser.all_fields.index(field_name)] for record in self.records)
        
    def extract_trackpoints_xml(self):
        """
        from a raw TCX file of the form :
        <Lap><Track>
          <Trackpoint></Trackpoint><Trackpoint></Trackpoint> ...n
        </Track></Lap> ...n
        
        in the form
        """
        num_records=0
        for lap in self.laps:
            
            TrackPoints = lap.Track.Trackpoint
            for trackpoint in TrackPoints:
                Record = []    
                
                for trackpoint_field in self.trackpoint_fields:  
                    list_append(Record,trackpoint,trackpoint_field)

                for trackpoint_value_field in self.trackpoint_value_fields:
                    list_append(Record,trackpoint,trackpoint_value_field,True)

                TPX = trackpoint.Extensions.TPX

                list_append(Record,TPX,"Watts")
                list_append(Record,TPX,"Speed")
                self.records.append(Record)

class TestTcxParser(unittest.TestCase):
    def setUp(self):
        pass

    def test_basic(self):
        
        self.expected_results = {"DistanceMeters":10,
                                 "HeartRateBpm":150,
                                 "Watts":300,
                                 "Speed":100}

        tcx = TcxParser("./test_files/test_basic.tcx")

        for key in self.expected_results.keys():
            self.assertEqual(tcx.get_field_val_by_name(0,key),
                             self.expected_results[key])

    def test_complex(self):
        
        self.expected_results = {"DistanceMeters":120,
                                 "HeartRateBpm":1860,
                                 "Cadence":1260,
                                 "Watts":1860,
                                 "Speed":1860}

        tcx = TcxParser("./test_files/test_complex.tcx")

        for key in self.expected_results.keys():
            self.assertEqual(tcx.get_field_sumval_by_name(key),
                             self.expected_results[key])
            
    def test_no_value_element(self):
        tcx = TcxParser("./test_files/test_no_value.tcx")
        self.assertEqual(tcx.get_field_val_by_name(0,"HeartRateBpm"),-1)

    def test_total_calories(self):
        'also tests multiple laps'
        tcx = TcxParser("./test_files/test_total_calories.tcx")
        self.assertEqual(tcx.get_total_calories(),200)

    def test_total_time(self):
        ' also tests multiple trackpoints'
        tcx = TcxParser("./test_files/test_total_time.tcx")
        self.assertEqual(tcx.get_total_lap_time(),120)

    def test_get_total_trackpoint_distance(self):
        tcx = TcxParser("./test_files/test_total_trackpoint_distance.tcx")
        self.assertEqual(tcx.get_total_trackpoint_distance(),40)
        
    def test_dump_to_csv(self):
        tcx = TcxParser("./test_files/test_complex.tcx")
        tcx.dump_to_csv()
        
        results = read_delim_text_from_file(self.dump_filename)
        expect_results =  read_delim_text_from_file("./test_files/test_complex_dump.csv")
        
        self.assertListEqual(results,expected_results)
        
    def tearDown(self):
        pass

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTcxParser)
    unittest.TextTestRunner(verbosity=2).run(suite)
