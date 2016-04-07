"""
Douglas Peucker compression algorithme
"""

#Author : Belfodil Aimene <aimene.belfodil@insa-lyon.fr>

from ....model import Trace


def _rdp_compress(trace,epsilon=0.0001) :
    """
    Perform the Ramer-Douglas-Peucker algorithm on the trace

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    epsilon : float, optional
        epsilon precise the maximal EUCLIDIAN DISTANCE supported in compression.
        Lesser is epsilon, better is the compression (in term of the distance between
        the compressed trace and the original trace)
        Note : default value is 0.0001 (in euclidian space) which is approximatly 11.132 meters

    Returns
    -------
    compressed_trace : Trace
        the compressed trace.

    Notes
    -----
    The computational complexity is O(n log(n))
    """
    
    positions_list=list(trace)
    compressed_events_list=_rdp_compress_recursive(positions_list,epsilon)
    trace=Trace()
    for event in compressed_events_list :
        trace.add_event(event)
    return trace

def _shortest_distance_to_segment(position,segment_starting_position,segment_ending_position) :
    """
    Calculate the shortest distance between a point and a segment

    Parameters
    ----------
    position : Position
        A Position object (see Position in Model)

    segment_starting_position : Position
        the starting position of the segment

    segment_ending_position : Position
        the ending position of the segment

    Returns
    -------
    shortest_distance : double
        the shortest distance between the point and the segment (in the euclidian space).
    """
    
    segment_length=segment_starting_position.euclidean_distance(segment_ending_position)
    
    if (segment_length==0) :
        return position.euclidean_distance(segment_starting_position)
    
    segment_length_sqr=segment_length*segment_length

    difference_latitude_with_starting_position=position.latitude-segment_starting_position.latitude
    difference_longitude_with_starting_position=position.longitude-segment_starting_position.longitude
    difference_latitude_in_segment=segment_ending_position.latitude-segment_starting_position.latitude
    difference_longitude_in_segment=segment_ending_position.longitude-segment_starting_position.longitude

    r=(difference_latitude_with_starting_position*difference_latitude_in_segment+
       difference_longitude_with_starting_position*difference_longitude_in_segment)/segment_length_sqr
    
    if (0<=r<=1) :
        s=(difference_latitude_with_starting_position*difference_longitude_in_segment-
           difference_longitude_with_starting_position*difference_latitude_in_segment)/segment_length_sqr
        return abs(s)*segment_length

    return min(position.euclidean_distance(segment_starting_position),position.euclidean_distance(segment_ending_position))


def _rdp_compress_recursive(positions_list,epsilon) :
    """
    Perform the Ramer-Douglas-Peucker algorithm on the trajectory

    Parameters
    ----------
    positions_list : list<Position>
        A list of Position (see Position in Model) which represent the trajectory

    epsilon : float, optional
        epsilon precise the maximal EUCLIDIAN DISTANCE supported in compression.
        Lesser is epsilon, better is the compression (in term of the distance between
        the compressed trace and the original trace)
        Note : default value is 0.0001 (in euclidian space) which is approximatly 11.132 meters

    Returns
    -------
    compressed_trace : positions_list
        the compressed trajectory.

    Notes
    -----
    The computational complexity is O(n log(n))

    References
    ----------
    Douglas, D. H., & Peucker, T. K. (1973). Algorithms for the reduction of the number of points
    required to represent a digitized line or its caricature.
    Cartographica: The International Journal for Geographic Information and Geovisualization, 10(2), 112-122.
    """
    
    dmax=0
    index=0
    for i in range(1,len(positions_list)-1) :
        d=_shortest_distance_to_segment(positions_list[i],positions_list[0],positions_list[-1])
        if (d>dmax) :
            index=i
            dmax=d
    if (dmax>epsilon) :
        sub_trajectory_1=_rdp_compress_recursive(positions_list[0:index],epsilon)
        sub_trajectory_2=_rdp_compress_recursive(positions_list[index:-1],epsilon)
        result=sub_trajectory_1+sub_trajectory_2
    else :
        result=[positions_list[0],positions_list[-1]]
    return result


class RDP_compression :
    """
    Perform the Ramer-Douglas-Peucker algorithm on the trace

    Parameters
    ----------
    epsilon : float, optional
        epsilon precise the maximal EUCLIDIAN DISTANCE supported in compression.
        Lesser is epsilon, better is the compression (in term of the distance between
        the compressed trace and the original trace)
        Note : default value is 0.0001 (in euclidian space) which is approximatly 11.132 meters

    Attributes
    ----------
    compressed_trace_ : Trace
        the compressed trace.

    Notes
    -----
    The computational complexity is O(n log(n))

    References
    ----------
    Douglas, D. H., & Peucker, T. K. (1973). Algorithms for the reduction of the number of points
    required to represent a digitized line or its caricature.
    Cartographica: The International Journal for Geographic Information and Geovisualization, 10(2), 112-122.
    """

    def __init__(self,epsilon=0.0001) :
        self.epsilon=epsilon

    def fit(self, trace) :
        """
        Perform the Ramer-Douglas-Peucker algorithm on the trace

        Parameters
        ----------
        trace : Trace
            A Trace object (see Trace in Model)

        Returns
        -------
        compressed_trace_ : Trace
            the compressed trace.
        """

        self.compressed_trace_=_rdp_compress(trace,epsilon=self.epsilon)
        return self.compressed_trace_
