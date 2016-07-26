
from scheduler_dates import day_enum, calendar_enum, event_type_enum

class EventLinkedList():
    
    event_anchors = {}
    
    def __init__(self):
        pass        
    
class Event():
    
    def __init__(self,prev_events,next_events,event_type):

        self.prev_events = prev_events #list of pointers to events; empty if terminus
        self.next_events = next_events #list of pointers to events
        self.event_type = event_type
        self.last_modified_time = self._now()
     
    @staticmethod
    def fromdict(cls,prev_event,next_event,event_type,**kwargs):
        
        cls1 = cls(prev_event,next_event,event_type)
        
        for key,value in args.iteritems():
            setattr(cls1,key,value)
        
    @staticmethod
    def fromkvlists(cls,prev_event,next_event,event_type,keys,values):
        cls1 = cls(prev_event,next_event,event_type)
        
        for i in range(len(keys)):
            setattr(cls1,keys[i],values[i])
            
    def _now(self):
        return(MyDT.now('US/Eastern').msecs)
    
    def amend(self):
        pass

db_config = get_config_from_schema("./test_schema.xml")

e = event.fromkvlists(None,None,event_type_enum.freetime,
                      db_config['col_defn'],