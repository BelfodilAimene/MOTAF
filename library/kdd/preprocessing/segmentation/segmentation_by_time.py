"""
Trace segmentation by time
"""

#Author : Belfodil Aimene <aimene.belfodil@insa-lyon.fr>

from ....model import Trace

def _segment_by_time(trace,maximum_time_difference=1800) :
    """
    Segment the trace in n segment where each segment is continous
    with respect to maximum_time_difference

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    maximum_time_difference : float, optional
        float value in seconds, two consecutive event which time
        difference exceed maximum_time_difference are in two
        different segments.

    Returns
    -------
    segmented_trace : list<Trace>
        the segmented trace as list of trace (all event are took in count).

    Notes
    -----
    The computational complexity is O(n)
    """
    
    segmented_trace=[]
    current_segment=Trace()
    last_event=None
    for current_event in trace :
        if (not last_event) :
            current_segment.add_event(current_event)
        elif (current_event.time_difference(last_event)<=maximum_time_difference) :
            current_segment.add_event(current_event)
        else :
            segmented_trace.append(current_segment)
            current_segment=Trace()
        last_event=current_event
    return segmented_trace


class Segmentation_by_time :
    """
    Segment the trace in n segment where each segment is continous
    with respect to maximum_time_difference.

    Parameters
    ----------
    maximum_time_difference : float, optional
        float value in seconds, two consecutive event which time
        difference exceed maximum_time_difference are in two
        different segments.

    Attributs
    ---------
    segmented_trace_ : list<Trace>
        the segmented trace as list of trace (all event are took in count).
    """

    def __init__(self,maximum_time_difference=1800) :
        self.maximum_time_difference=maximum_time_difference

    def fit(self, trace) :
        """
        Segment the trace in n segment where each segment is continous
        with respect to maximum_time_difference.

        Parameters
        ----------
        trace : Trace
            A Trace object (see Trace in Model)

        Returns
        -------
        segmented_trace_ : list<Trace>
            the segmented trace as list of trace (all event are took in count).
        """

        self.segmented_trace_=_segment_by_time(trace,maximum_time_difference=self.maximum_time_difference)
        return self.segmented_trace_
