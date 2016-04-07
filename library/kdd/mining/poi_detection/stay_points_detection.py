"""
Stay point detection
"""

#Author : Belfodil Aimene <aimene.belfodil@insa-lyon.fr>

from ....model import Stay_point

def _stay_points_detection(trace,dist_thres=0.0001,time_thres=1800) :
    """
    Perform stay point detection from a trace.

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    dist_thres : float, optional
        precise the distance threshold (in euclidean space) to be used
        default value is 0.0001 (approximately 11.132 meters) 

    time_thres : float, optional
        precisie the time threshold (in seconds) to be used

    Returns
    -------
    stay_points : list<Stay_point>
        A list of Stay_point object (see Stay_point in Model)

    References
    ----------
    Li, Q., Zheng, Y., Xie, X., Chen, Y., Liu, W., & Ma, W. Y. (2008, November).
    Mining user similarity based on location history.
    In Proceedings of the 16th ACM SIGSPATIAL international conference
    on Advances in geographic information systems (p. 34). ACM. 
    """
    
    i=0
    stay_points=[]
    trace_size=len(trace)
    while i<trace_size :
        point_i=trace[i]
        points_list=[]
        token=False
        j=i+1
        while j<trace_size :
            points_list.append(trace[j-1])
            point_j=trace[j]
            distance=point_i.euclidean_distance(point_j)
            if (distance>dist_thres) :
                time_difference=point_j.time_difference(point_i)
                if (time_difference>=time_thres) :
                    stay_point_latitude=0
                    stay_point_longitude=0
                    for point in points_list :
                        stay_point_latitude+=point.latitude
                        stay_point_longitude+=point.longitude
                    stay_point_latitude  /= len(points_list)
                    stay_point_longitude /= len(points_list)
                    stay_point_arrival    = point_i.datetime
                    stay_point_departure  = point_j.datetime
                    stay_point=Stay_point(stay_point_latitude,stay_point_longitude,stay_point_arrival,stay_point_departure,label="stay point {0}".format(len(stay_points)+1))
                    stay_points.append(stay_point)
                    i=j
                    token=True
                break
            j+=1
        if (not token) : i+=1
    return stay_points


class Stay_points :
    """
    Perform stay point detection from a trace.

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    dist_thres : float, optional
        precise the distance threshold (in euclidean space) to be used

    time_thres : float, optional
        precisie the time threshold (in seconds) to be used

    Attributs
    -------
    stay_points_ : list<Stay_point>
        A list of Stay_point object (see Stay_point in Model)

    References
    ----------
    Li, Q., Zheng, Y., Xie, X., Chen, Y., Liu, W., & Ma, W. Y. (2008, November).
    Mining user similarity based on location history.
    In Proceedings of the 16th ACM SIGSPATIAL international conference
    on Advances in geographic information systems (p. 34). ACM.
    """

    def __init__(self,dist_thres=0.0001,time_thres=1800) :
        self.dist_thres=dist_thres
        self.time_thres=time_thres

    def fit(self, trace) :
        """
        Perform stay point detection from a trace.

        Parameters
        ----------
        trace : Trace
            A Trace object (see Trace in Model)

        Returns
        -------
        stay_points_ : list<Stay_point>
            A list of Stay_point object (see Stay_point in Model)
        """

        self.stay_points_=_stay_points_detection(trace,dist_thres=self.dist_thres,time_thres=self.time_thres)
        return self.stay_points_
