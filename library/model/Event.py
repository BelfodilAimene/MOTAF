from Position import Position
    
class Event(Position) :

    def __init__(self,datetime,longitude,latitude) :
        self.datetime=datetime
        Position.__init__(self,longitude,latitude)

    def time_difference(self,other) :
        """
        return time difference in seconds between the two event (in absolute value)
        """
        return (self.datetime-other.datetime).total_seconds()

    def __str__(self) :
        return "({0},{1})".format(str(self.datetime),Position.__str__(self))
