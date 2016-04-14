from datetime import datetime,timedelta
from time import strftime
from time import time
from pytz import timezone, common_timezones

class InvalidTimezone(Exception):
    pass

class MyTZ(object):

    #print len(common_timezones)
    #print common_timezones

    def __init__(self,tz_str):
        self.tz_str = self.validate(tz_str)
        self.tz = timezone(self.tz_str)
        

    def validate(self,tz_str):
        if not tz_str in common_timezones:
            raise InvalidTimezone(tz_str)
        return(tz_str)
        
    @property
    def value(self):
        return(self.tz)

class MyDTInvalidConstructorArgs(Exception):
    pass

class MyDT(object):
    '''
    default - take a dt object and provide ways to adjust base and
    display timezones and formats

    str construct - take a dt str and format

    '''

    @classmethod
    def str(cls,tz_str,**kw):
        dt = datetime.strptime(kw.__getitem__('dt_str'),
                               kw.__getitem__('dt_str_fmt'))
        return(cls(dt,tz_str,**kw))
    
    @classmethod
    def secs(cls,tz_str,secs,**kw):
        dt = datetime.utcfromtimestamp(secs)
        return(cls(dt,tz_str,**kw))

    @classmethod
    def now(cls,tz_str='US/Eastern',**kw):
        dt = datetime.now()
        return(cls(dt,tz_str,**kw))

    @classmethod
    def midnight_today(cls,tz_str,**kw):
        dt = datetime.now().replace(hour=0, minute=0, second=0,microsecond=0)
        return(cls(dt,tz_str,**kw))


    def __init__(self,dt,tz_str='US/Eastern',**kw):
        [setattr(self,k,v) for k,v in kw.iteritems()]

        self.tz = MyTZ(tz_str)
        self.dt = self.add_tz(dt,self.tz)
        self.secs = self.dt_to_secs(self.dt,self.tz)
        self.msecs = (self.dt_to_secs(self.dt,self.tz) * 1000000)+self.dt.microsecond
                
        if not kw.has_key('display_fmt'):
            self.display_fmt = '%m/%d/%Y %H:%M:%S %Z %z'
        if not kw.has_key('display_tz_str'):
            self.display_tz = self.tz
        else:    
            self.display_tz = MyTZ(self.display_tz_str)
        if kw.has_key('day_offset'):
            self.dt = self.dt + timedelta(days=1)

        self.value = self.dt_to_str_fmt(self.dt,self.display_fmt,self.display_tz)


    def __call__(self):
        print self.value

    def __str__(self):
        return(self.value)

    def get_secs(self):
        return(self.secs)

    def time_to_secs():
        '''
        take a time in hours,mins & secs and return number of ms
        '''
        pass 

    def dt_to_secs(self,dt,tz):
        '''
        take a datetime object and return seconds since epoch
        '''
        origin  = self.add_tz(datetime(1970,1,1,0,0,0),tz)
        return(int((dt-origin).total_seconds()))

    def str_fmt_to_dt(self,dt_str,dt_str_fmt,tz):
        '''
        take a str of format fmt and return a datetime object
        '''
        self.dt = datetime.strptime(dt_str, dt_str_fmt)
        self.dt = self.add_tz(self.dt,tz)

    def dt_to_str_fmt(self,dt,display_fmt,display_tz):
        '''
        take a datetime object and return a str of format fmt
        '''
        dt_adj = self.display_astimezone(dt,display_tz)
        dt_display_str = dt_adj.strftime(display_fmt)
        return(dt_display_str)

    def display_astimezone(self,dt,display_tz):
        return(dt.astimezone(display_tz.value))

    def add_tz(self,dt,tz):
        return(tz.value.localize(dt, is_dst=True))

if __name__ == '__main__':

    dt = datetime.now()
    # to run the below manually use the following syntax
    # mydt = MyDT(args,kw) so for 1 MyDT(dt,'US/Eastern')
    # and to return now in %H:%M:%S
    # mydt = MyDT.now(display_fmt='%H:%M:%S')
    #exit()

    # this works, inputting a microsecond precision
    mydt = MyDT.str('US/Eastern',
             dt_str='1:23:45.67890',
             dt_str_fmt='%H:%M:%S.%f')
    print mydt.msecs

    exit()
    
    runs = [
        {
            #to dt obj, assign base tz of Europe/London',
            'cls':'MyDT',
            'args':[dt,'Europe/London'],
            'kw'   :{}
        },
        {
            #to dt obj, assign base tz of US/Eastern'
            #timezone string is blank so defaults to US/Eastern,
            'cls':'MyDT',
            'args':[dt],
            'kw'   :{}
        },
            
        {
            #to dt obj, assign base tz of US/Eastern
            #alter display fmt to %H:%M:%S %Z %z and
            #display tz to Europe/London'
            'cls':'MyDT',
            'args':[dt,'US/Eastern'],
            'kw':{'display_fmt'   :'%H:%M:%S %Z %z',
                  'display_tz_str':'Europe/London'}
        },
        {
            'cls':'MyDT',
            'clsmthd':'str',
            'args':['Europe/London'],
            'kw':{'dt_str':'4/14/2014 11:12:13',
                  'dt_str_fmt':'%m/%d/%Y %H:%M:%S'}
        },
        {
            'cls':'MyDT',
            'clsmthd':'str',
            'args':['US/Eastern'],
            'kw':{'dt_str':'4/14/2014 11:12:13',
                  'dt_str_fmt':'%m/%d/%Y %H:%M:%S',
                  'display_fmt':'%H:%M:%S %Z %z',
                  'display_tz_str':'Europe/London'}
        },
        {
            'cls':'MyDT',
            'clsmthd':'secs',
            'args':['US/Eastern',1937872748],
            'kw':{'display_fmt':'%H:%M:%S %Z %z',
                  'display_tz_str':'Europe/London'}
        },
        {
            'cls':'MyDT',
            'clsmthd':'now',
            'args':['US/Eastern'],
            'kw':{'display_fmt':'%H:%M:%S %Z %z',
                  'display_tz_str':'Europe/London'}
        },
        {
            'cls':'MyDT',
            'clsmthd':'midnight_today',
            'args':['US/Eastern'],
            'kw':{'display_fmt':'%m/%d/%Y %H:%M:%S %Z %z',
                  'day_offset':1}
        },
        {
            'cls':'MyDT',
            'clsmthd':'midnight_today',
            'args':['US/Eastern'],
            'kw':{'display_fmt':'%m/%d/%Y %H:%M:%S %Z %z'}
        },
        {
            # display format is seconds since epoch
            'cls':'MyDT',
            'args':[dt,'US/Eastern'],
            'kw':{'display_fmt':'%s'}
        }
        ]
        
    for r in runs:
        arg=r.__getitem__('args')
        kw=r.__getitem__('kw')
        cls=globals()[r.__getitem__('cls')]
        if r.has_key('clsmthd'):
            clsmthd=getattr(cls,r.__getitem__('clsmthd'))
            print clsmthd(*arg,**kw)
        else:
            print cls(*arg,**kw)
