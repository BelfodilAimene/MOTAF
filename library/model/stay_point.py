from position import Position
    
class Stay_point(Position) :
    """
    This class models a stay point.

    Parameters
    ----------

    latitude : float
        the latitude of the moving object at the datetime moment

    longitude : float
        the longitude of the moving object at the datetime moment

    starting_time : Datetime
        the arrival time in the position

    ending_time : Datetime
        the departure time from the position

    label : string, optional
        the label of the stay_point (empty by default)
    
    
    Attributes
    ----------

    latitude : float
        the latitude of the moving object at the datetime moment

    longitude : float
        the longitude of the moving object at the datetime moment

    starting_time : Datetime
        the arrival time in the position

    ending_time : Datetime
        the departure time from the position

    label : string
        the label of the stay_point (empty by default)
    """

    def __init__(self,latitude,longitude,starting_time,ending_time,label="") :
        Position.__init__(self,latitude,longitude)
        self.starting_time=starting_time
        self.ending_time=ending_time
        self.label=label

    def __str__(self) :
        return "({0},{1} -> {2}, {3})".format(Position.__str__(self),self.starting_time,self.ending_time,self.label)
