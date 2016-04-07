class Trace :
    """
    This class models a Mobility Trace of a moving object in time.
    The trace is seen as a list of events :
    (__list__, __getitems__, __iter__ and __len__ methods are overloaded)

    Attributes
    ----------

    __events : list<Event>
        list of event ordered by increasing datetime (by construction) 
    """
    
    def __init__(self) :
        self.__events=[]

    def add_event(self,event) :
        self.__events.append(event)
        
    def add_events(self,*events) :
        self.__events.extend(events)

    def __len__(self) :
        return len(self.__events)

    def __list__(self) :
        return self.__events

    def __getitem__(self,key) :
        return self.__events[key]

    def __iter__(self) :
        return iter(self.__events)

    
    
