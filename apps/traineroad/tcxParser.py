#!/usr/bin/python
import xml.etree.ElementTree as xmltree
from datetime_util import MyDT
from db_utils import T_PKEY, Database,DatabaseRecord, DatabaseTable, DBErrorDupePKeyInsert,DBErrorRecSchemaInvalid, DBErrorZeroDataRecords

def _get_secs(timestr):
    mydt = MyDT.str('US/Eastern',dt_str=timestr,dt_str_fmt='%Y-%m-%dT%H:%M:%SZ')
    return(mydt.secs)

def parse_tcx(filen, ns):
    
    trackpoints = xmltree.parse(filen).findall('.//tcx:Trackpoint',ns)
    
    # get the time in secs of first Trackpoint so can calculate # of secs from start
    time = trackpoints[0].find('tcx:Time',ns)    
    start_time = _get_secs(time.text) -1

    tplist = []
    
    for trackpoint in trackpoints:
        
        tpdict = {}
        distance = trackpoint.find('tcx:DistanceMeters',ns)
        cadence = trackpoint.find('tcx:Cadence',ns)
        
        heartratebpm = trackpoint.find('tcx:HeartRateBpm',ns)
        heartratebpmvalue = heartratebpm.find('tcx:Value',ns)
        
        watts = trackpoint.find('.//ns3:Watts',ns)
        speed = trackpoint.find('.//ns3:Speed',ns)
        
        time = trackpoint.find('tcx:Time',ns)    
        mydt = MyDT.str('US/Eastern',dt_str=time.text,dt_str_fmt='%Y-%m-%dT%H:%M:%SZ')
        
        time_secs = _get_secs(time.text)
        
        tpdict['time_secs'] = int(time_secs-start_time)
        tpdict['cadence'] = int(cadence.text)
        tpdict['heartratebpmvalue'] = int(heartratebpmvalue.text)
        tpdict['watts'] = int(watts.text)
        tpdict['speed'] = round(float(speed.text),1)
        
        tplist.append(tpdict)
    
    return(tplist)

class Workouts(Database):
    pass

class Trackpoints(DatabaseTable):
    def __init__(self):
        super(Trackpoints,self).__init__()
        self._set_pk("time_secs")

    def _set_pk(self,pk_value):
        setattr(self,T_PKEY,pk_value)
        
    def _get_pk(self):
        return(getattr(self,T_PKEY))
    
    def rec_exists(self,pk):
        return(self.has_key(pk))
    
    def add(self,**kwargs):
        new_dr = DatabaseRecord(self,**kwargs)

        pkey = new_dr._get_pk()

        if self.rec_exists(pkey):            
            # check _allow_amend_dupe_insert flag, if True then assume 
            # that this is an update of an existing otherwise raise an exception
            # as this is dupe key
            if not self._allow_amend_dupe_insert:
                raise DBErrorDupePKeyInsert(pkey)

            # get orig record         
            orig_dr = self[pkey]

            # make orig record the old version
            new_dr._set_old_version(pkey,orig_dr)

            # overwrite old record in table with new record
            self[pkey] = new_dr

            # set new rec as dirty so we know to update into gadflydb
            new_dr._set_dirty(pkey)

            # return the new record
            return(self[pkey])
        else:
            self[pkey] = new_dr

        new_dr._set_dirty(pkey)
        self._record_count+=1
        return(new_dr)
    
    def add_list(self,records):
        assert isinstance(records,list)
        for rec in records:
            self.add(**rec)
            
            
filen="/home/burtnolej/pythonapps3/trainerroad/test_files/test_small.tcx"
ns={'tcx':'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2',
    'ns3':'http://www.garmin.com/xmlschemas/ActivityExtension/v2'}

_trackpoints = parse_tcx(filen,ns)

workout = Workouts("/usr/lib/python2.7/dist-packages/gadfly/scripts/","auto")

trackpoints = workout.table(Trackpoints) # create table object instance   
trackpoints.add_list(_trackpoints) # add record to table obj inst
workout.init_objects_in_db() # create table in gadflydb
workout.commit_to_gf() # add records to gadflydb
workout.close()