# -*- coding: utf-8 -*-
from sys import path,stdout,argv
import sys
path.append("/Users/burtnolej/Dev/pythonapps/util")
from filesystem_util import read_file_delim, read_dir
from datetime_util import MyDT
from os import path
import numpy as np

valid_config_keys=['header','delim','mavg','mavg_unit','dir_name','datfile_delim','dir_ext']
valid_mavg_units=['NO_SAMPLES']
valid_delims=['\t',',']

valid_headers=['Index','Elapsed time [h:mm:ss.hh]','Elapsed time total [h:mm:ss.hh]',"Turns number [Nr]","Cadence [rpm]","Cadence peak [rpm]","Cadence average [rpm]","Circ. pedal velocity [m/s]","Speed [km/h]","Avr speed [km/h]","Distance [m]","Distance total [m]","Heart rate [bpm]","Heart rate peak [bpm]","Heart rate average [bpm]","Force per revolution [N]","Force peak total [N]","Force peak [N]","Avr force [N]","Torque [Nm]","Avr torque [Nm]","Pace/1000m [sec]","Avr pace/1000m [sec]","Power [W]","Power peak [W]","Avr power [W]","Power/Kg [W/Kg]","Avr power/Kg","[W/Kg]","Calories [cal]","Calories total [Kcal]","Work [J]","Work total [KJ]","Left leg percent [%]","Total left leg percent [%]","Right leg percent [%]","Total right leg percent [%]","Left time to force peak [mm:ss:00]","Total left time to force peak [mm:ss:00]","Right time to force peak [mm:ss:00]","Total right time to force peak [mm:ss:00]","Left angle to force peak [°]","Total left angle to force peak [°]","Right angle to force peak [°]","Total right angle to force peak [°]"]

class UnknownHeaderException(Exception):
    pass
class MissingConfigException(Exception):
    pass
class InvalidMAVG_UNITException(Exception):
    pass
class InvalidDATFILE_DELIMException(Exception):
    pass
class InvalidDELIMException(Exception):
    pass
class InvalidDIR_NAMEException(Exception):
    pass
class MAVGOutOfRangeException(Exception):
    pass
class DatFileNotFoundException(Exception):
    pass
class InvalidIndexException(Exception):
    pass
    
def split_filename(abs_fn):
    '''
    check if filename is in the format './d1/d2/dirn/%m-%d-%Y_%i.dat'
    where i is an integer representing the interval
    '''
    try:
        rel_fn = abs_fn.split("/")[-1]
        pre_fn = rel_fn.split(".")[0]
        date,idx = pre_fn.split("_")
        m,d,Y = date.split("-")
        assert MyDT.str('US/Eastern',
                       dt_str=m+d+Y,
                        dt_str_fmt='%m%d%Y')
        assert int(idx)
    except AssertionError:
        raise AssertionError
    except ValueError:
        raise ValueError
    
    return(date,idx)

def read_wattbike_dat_dir(dirname,DIREXT):
    # expects filename 05-24-2014_7.dat

    try:
        l = read_dir(dirname,DIREXT)
    except OSError:
        print 'Error',dirname,'not a dir'
        exit()

    j=[]
    for abs_fn in l:
        try:
            date,idx = split_filename(abs_fn)
            j.append((date,idx,abs_fn))
        except ValueError,AssertionError:
            print 'Error',abs_fn,'not in format %m-%d-%Y_%i'

    return(j)

def get_timedelta_msecs(timedelta):
    '''
    checks if timedelta in format %H:%M:%S.%f
    returns timedelta in microseconds 
    '''
    try:
        secs,msecs = timedelta.split(".")
        assert int(msecs)
    
        secs_l = secs.split(":") # h,m,s
        assert len(secs_l) == 3
    
        secs = (int(secs_l[0]) * 60 * 60) + (int(secs_l[1]) * 60) + int(secs_l[2])
    except ValueError:
        raise ValueError

    return((secs * 1000000)+int(msecs))
    
def read_wattbike_dat(filename,delim):
    if delim not in valid_delims:
        raise InvalidDelimException
    
    try:
        header,records = read_file_delim(filename,delim,True)
    except IOError:
        raise DatFileNotFoundException

    r_new=[]
    for r in records:
        f_new=[]
        for f in r:
            # see if we can convert to int, if not try time
            try:
                f_new.append(float(f))
            except ValueError:
                try:
                    f_new.append(int(f))
                except ValueError:
                    try: # convert to msecs if you can otherwise str
                        f_new.append(get_timedelta_msecs(f))
                    except:
                        f_new.append(str(f))
                
        r_new.append(f_new)

    print 'Log',filename,'processed'
    return(r_new)

def process_wattbike_cfg(**kwargs):
    '''
    read in a config variables, validate and process
    will return the index of the fields in the dat file
    
    minimum args expected are:
      valid_config_keys, valid_headers, valid_mavg_units, valid_delim
      headers, delim, mavg, mavg_unit, dir_name, datfile_delim, dir_ext 
    '''
    try:
        for k in valid_config_keys:
            kwargs[k]
    except:
        raise MissingConfigException(k)
    
    fields = kwargs['header'].split(kwargs['delim'])

    # validate that config values are ok
    field_indexes=[]
    for f in fields:
        try:
            index = kwargs['valid_headers'].index(f)
            field_indexes.append(index)
        except ValueError:
            raise UnknownHeaderException(f)

    if kwargs['mavg'] < 0 or kwargs['mavg'] > 100:
        raise MAVGOutOfRangeException(kwargs['mavg'])

    if not kwargs['mavg_unit'] in kwargs['valid_mavg_units']:
        raise InvalidMAVG_UNITException(kwargs['mavg_unit'])

    if not kwargs['delim'] in kwargs['valid_delims']:
        raise InvalidDELIMException(kwargs['delim'])

    if not kwargs['datfile_delim'] in kwargs['valid_delims']:
        raise InvalidDATFILE_DELIMException(kwargs['datfile_delim'])

    if not path.isdir(kwargs['dir_name']):
        raise InvalidDIR_NAMEException(kwargs['dir_name'])

    return(field_indexes)

class InvalidWeight(Exception):
    pass

class InvalidWeightMoreThanTSLen(Exception):
    pass
    
def timeseries2mavg(**kw):
    '''
    take a timeseries(ts) and return a moving average of that ts
    based on a window size of n
    if n divides into len(ts) with no remainder then there
    will be len(ts)/n datapoints returned and if not len(ts)/n + 1  
    '''
    mavg = [] # resulting time series

    for k,v in kw.iteritems():
        globals()[k] = v

    if weight < 0:
        raise InvalidWeight(weight)

    if weight > len(timeseries):
        raise InvalidWeightMoreThanTSLen(weight,len(timeseries))
        
    r = len(timeseries)%weight # remainder

    if r>0:
        # process remainder # of rows
        st=0
        for j in range(r):
            st = st + timeseries[j]
        mavg.append(st/float(r))

    # skip remainder to get tranches of size mavg
    for i in range(r,len(timeseries),weight):
        # for 1 tranche of size mavg
        st = 0 # subtotal
        for j in range(i,i+weight):
            st = st + timeseries[j]
        mavg.append(st/float(weight))
    return(mavg)
    
    
def analyse(records,idx,mavg):
    results = []
    for i in range(0,len(idx)):
        ts = []
        for j in range(len(records)):
            ts.append(records[j][i])
        results.append(timeseries2mavg(ts,mavg))    
    return(results)


#field_index,config=read_wattbike_cfg(config_filename,VALID_HEADERS,VALID_UNITS,VALID_KEYS)

 
#files = read_wattbike_dat_dir(config['DIR_NAME'],config['DIR_EXT'])

#for date,interval,fn in files:
#    records = read_wattbike_dat(fn,cfg['DATFILE_DELIM'])
#    analyse(records,,cfg['MAVG'])
