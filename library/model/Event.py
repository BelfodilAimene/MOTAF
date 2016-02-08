from position import Position
    
class Event(Position) :
    """
    This class models an Event.

    Parameters
    ----------

    datetime : datetime.datetime (datetime python package)
        object of type datetime.datetime (datetime package)
        which precise the moment where the event is recorded

    latitude : float
        the latitude of the moving object at the datetime moment

    longitude : float
        the longitude of the moving object at the datetime moment
    
    
    Attributes
    ----------

    datetime : datetime.datetime (datetime python package)
        object of type datetime.datetime (datetime package)
        which precise the moment where the event is recorded

    latitude : float
        the latitude of the moving object at the datetime moment

    longitude : float
        the longitude of the moving object at the datetime moment
    """

    def __init__(self,datetime,latitude,longitude) :
        self.datetime=datetime
        Position.__init__(self,latitude,longitude)

    def time_difference(self,other) :
        """
        Return time difference in seconds between the two event (from other event to self event)
        If 'other' event occured after 'self' event, the time_difference will be negative.

        Parameters
        ----------

        other : Event
            Object of class Event

        Returns
        -------
        
        time_difference : float
            time difference in seconds between the two event (from other event to self event)
        """
        
        return (self.datetime-other.datetime).total_seconds()

    def __str__(self) :
        return "({0},{1})".format(str(self.datetime),Position.__str__(self))
