import math,numpy as np
from const import Const 

class Position :
    """
    This class models a Position in earth.

    Parameters
    ----------

    latitude : float
        the latitude of the moving object at the datetime moment

    longitude : float
        the longitude of the moving object at the datetime moment
    
    
    Attributes
    ----------

    latitude : float
        the latitude of the mouving object at the datetime moment

    longitude : float
        the longitude of the mouving object
    """

    def __init__(self,latitude,longitude) :
        self.latitude=float(latitude)
        self.longitude=float(longitude)
    
    def geodisic_distance(self,other) :
        """
        Return geodisic distance between two points in earth in meter

        Parameters
        ----------

        other : Event
            Object of class Event

        Returns
        -------
        
        distance : float
            geodisic distance between two points in earth in meter
        """
        
        latitude1,longitude1,latitude2,longitude2=self.latitude,self.longitude,other.latitude,other.longitude
        if (latitude1==latitude1 and longitude1==longitude2) : return 0
        const = Const()
        earth_radius=const.earth_radius
        degrees_to_radians = math.pi/180
        phi1 = (90.0 - latitude1)*degrees_to_radians
        phi2 = (90.0 - latitude2)*degrees_to_radians
        theta1 = longitude1*degrees_to_radians
        theta2 = longitude2*degrees_to_radians 
        cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
        if (cos>1) : cos=1
        elif (cos<-1) : cos=-1
        arccos = math.acos( cos )
        return earth_radius*arccos

    def euclidean_distance(self,other) :
        """
        Return euclidean distance between the two positions
        (latitude, longitude) are seen in the euclidean space (not spheric space)
        its a good approximation with the geodisic distance when the two points
        aren't distant.
        The distance unit isn't meter, we can say that 0.00001 is approximately 1 meter . 

        Parameters
        ----------

        other : Event
            Object of class Event

        Returns
        -------
        
        distance : float
            euclidean distance between the two positions
        """
        
        latitude1,longitude1,latitude2,longitude2=self.latitude,self.longitude,other.latitude,other.longitude
        latitude_difference,longitude_difference=latitude2-latitude1,longitude2-longitude1
        return math.sqrt(latitude_difference*latitude_difference+longitude_difference*longitude_difference)

    def bearing(self,other) :
        """
        Return the bearing from the self event to other event in degree between 0 and 360. 

        Parameters
        ----------

        other : Event
            Object of class Event

        Returns
        -------
        
        bearing : float
            The bearing from the self event to other event in degree between 0 and 360.
        """
        
        latitude1,longitude1,latitude2,longitude2=self.latitude,self.longitude,other.latitude,other.longitude
        radians_to_degrees = 180 / math.pi
        longitude_difference=longitude2-longitude1
        y = math.sin(longitude_difference) * math.cos(latitude2)
        x = math.cos(latitude1)*math.sin(latitude2) - math.sin(latitude1)*math.cos(latitude2)*math.cos(longitude_difference)
        bearing = math.atan2(y, x)*radians_to_degrees
        if (bearing<0) : bearing+=360
        return bearing

    def __str__(self) :
        return str((self.latitude,self.longitude))
