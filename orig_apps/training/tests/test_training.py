# -*- coding: utf-8 -*-
from sys import path,stdout,argv
import sys
path.append("..")
from training import process_wattbike_cfg,UnknownHeaderException, MissingConfigException,MAVGOutOfRangeException, InvalidWeight,InvalidWeightMoreThanTSLen,analyse, timeseries2mavg
import copy
import xml.etree.ElementTree as xmltree
from collections import namedtuple
from test_util import Tester, run_tests

class TestUnexpectedResult(Exception):
    pass

class TestTimeseries2MAVG(Tester):
    def __init__(self,descr,pos_test,exception,**kw):
        self.timeseries = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
        self.results = [1,2.5,4.5,6.5,8.5,10.5,12.5,14.5]
        self.weight = 2

        # start the test
        self.test(descr,pos_test,exception,**kw)

    def run(self):
        # call test function
        mavg=timeseries2mavg(
            timeseries=self.timeseries,
            weight=self.weight)

        if mavg != self.results:
            raise TestUnexpectedResult(mavg)

   # lets try to get all of the generic stuff into Tester
   # so the results test and invokation of test()
    
class TestReadWattbikeCFG(Tester):
    def __init__(self,*arg,**fields):
        # set values for the minimum set of args (inputs) the
        # function being tested needs to receive
        # these an be removed or modified by Tester.test() for the
        # purposes of creating test scenarios
        self.header='Power [W],Elapsed time [h:mm:ss.hh],Heart rate [bpm]'
        self.delim=','
        self.mavg=10
        self.mavg_unit='NO_SAMPLES'
        self.dir_name='.'
        self.datfile_delim='\t'
        self.dir_ext='dat'
        self.valid_delims=['\t',',']
        self.valid_config_keys=['header','delim','mavg','mavg_unit','dir_name','datfile_delim','dir_ext']
        self.valid_mavg_units=['NO_SAMPLES']
        self.valid_headers=["Index", #1
                       "Elapsed time [h:mm:ss.hh]", #2
                       "Elapsed time total [h:mm:ss.hh]", #3
                       "Turns number [Nr]", #4
                       "Cadence [rpm]", #5
                       "Cadence peak [rpm]", #6
                       "Cadence average [rpm]", #7
                       "Circ. pedal velocity [m/s]", #8
                       "Speed [km/h]", #9
                       "Avr speed [km/h]", #10
                       "Distance [m]", #11
                       "Distance total [m]", #12
                       "Heart rate [bpm]", #13
                       "Heart rate peak [bpm]", #14
                       "Heart rate average [bpm]", #15
                       "Force per revolution [N]", #16
                       "Force peak total [N]", #17
                       "Force peak [N]", #18
                       "Avr force [N]", #19
                       "Torque [Nm]", #20
                       "Avr torque [Nm]", #21
                       "Pace/1000m [sec]", #22
                       "Avr pace/1000m [sec]", #23
                       "Power [W]", #24
                       "Power peak [W]", #25
                       "Avr power [W]", #26
                       "Power/Kg [W/Kg]", #27
                       "Avr power/Kg", #28
                       "[W/Kg]", #29
                       "Calories [cal]", #30
                       "Calories total [Kcal]", #31
                       "Work [J]", #32
                       "Work total [KJ]", #33
                       "Left leg percent [%]", #34
                       "Total left leg percent [%]", #35
                       "Right leg percent [%]", #36
                       "Total right leg percent [%]", #37
                       "Left time to force peak [mm:ss:00]", #38
                       "Total left time to force peak [mm:ss:00]", #39
                       "Right time to force peak [mm:ss:00]", #40
                       "Total right time to force peak [mm:ss:00]", #41
                       "Left angle to force peak [°]", #42
                       "Total left angle to force peak [°]", #43
                       "Right angle to force peak [°]", #44
                       "Total right angle to force peak [°]"] #45

        # set the expected results
        self.results = [23,1,12]

        # start the test
        self.test(*arg,**fields)

    def run(self):
        kw={}
        # build kw list based on current member vars. some of these
        # may have been modified from default set in __init__() by
        # Tester.test()
        for k in self.valid_config_keys:
            if hasattr(self,k):
               kw[k] = getattr(self,k)

        # call test function
        field_index=process_wattbike_cfg(
            valid_config_keys=self.valid_config_keys,
            valid_headers=self.valid_headers,
            valid_mavg_units=self.valid_mavg_units,
            valid_delims=self.valid_delims,
            **kw)

        if field_index != self.results:
            raise TestUnexpectedResult(field_index)
        
Tests = {'obj':'TestReadWattbikeCFG',
         'tests':[(
                'Test a header specified in config but doesnt exist',
                'UnknownHeaderException',
                'header',
                'Power [W],Elapsed time [h:mm:ss.hh]x,Heart rate [bpm]',
                'Power [W],Elapsed time [h:mm:ss.hh],Heart rate [bpm]'
                ),
                (
                 'Test a mandatory config is not set',
                 'MissingConfigException',
                 'header',
                 None,
                 'Power [W],Elapsed time [h:mm:ss.hh],Heart rate [bpm]'
                ),
                (
                'Test a mandatory config is not set',
                'MissingConfigException',
                'mavg',
                None,
                10
                ),
                (
                'Test MAVG not in range',
                'MAVGOutOfRangeException',
                'mavg',
                1000,
                50
                ),
                (
                'Test invalid output/results',
                'TestUnexpectedResult',
                'results',
                [45,6,5],
                [23,1,12],
                )

                ]
            }


run_tests("./tests.xml")
