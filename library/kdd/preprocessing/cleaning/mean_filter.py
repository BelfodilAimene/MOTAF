"""
Mean Filter
"""

#Author : Belfodil Aimene <aimene.belfodil@insa-lyon.fr>

from ....model import Event


def _mean_filter(trace,window_size=4,window_type='causal',neighbooring_type='number') :
    """
    Perform a mean filter on the trace.

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    window_size : int, optional
        precise the size of the window used for filtering depends on neighbooring_type parameter
        if neighbooring_type='number' the window_size will precise the approximate number of event
        used; if neighbooring_type='time' the window_size will precise the size of window in seconds 

    window_type : {'causal', 'centered'}, optional
        'causal' : the filter is causal, thus, it use only actual and past events for each event
        'centered' : the filter is not causal, thus, it use past and futur events for each event

    neighbooring_type : {'number', 'time'}, optional
        the neighbooring_type change the signification of the window size, wether the neighbooring is
        calculated by time or just by order

    Returns
    -------
    filtered_trace : Trace
        the filtered trace.

    Notes
    -----
        - The commputational complexity is O(n)
        - The used distance is the euclidean distance.
    """
    
    if (window_type=='causal') : kernel_shape=(-window_size,0)
    elif (window_type=='centered') : kernel_shape=(-(window_size/2),window_size/2)
    else : raise Exception("window_type dosen't exists")

    if (neighbooring_type=='number') : filtered_trace=_base_mean_filter(trace,kernel_shape)
    elif (neighbooring_type=='time') : filtered_trace=_base_mean_filter_by_time(trace,kernel_shape)
    else : raise Exception("neighbooring_type dosen't exists")

    return filtered_trace


def _base_mean_filter(trace,kernel_shape) :
    """
    Perform a mean filter on the trace

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    kernel_shape : 2-tuple 
        the kernel_shape is 2-tuple (l,r) where l<=0 and r>=0, thus, when the filter
        estimate the position of an event of index 'i', it will use all the events of
        index in the interval [i+l,i+r]

    Returns
    -------
    filtered_trace : Trace
        the filtered trace.

    Notes
    -----
    The commputational complexity is O(n)
    """
    
    trace_size=len(trace)
    filtered_trace=[]
    
    left_index,right_index=kernel_shape

    neighboors=trace[0:right_index+1]
    neighboors_size=len(neighboors)
    latitudes,longitudes=zip(*[(position.latitude,position.longitude) for position in neighboors])
    sum_latitudes,sum_longitudes=sum(latitudes),sum(longitudes)

    event=Event(trace[0].datetime,sum_latitudes/neighboors_size,sum_longitudes/neighboors_size)
    filtered_trace.append(event)

    for i in xrange(1,trace_size) :

        if (left_index>=0) :
            most_left_event=trace[left_index]
            sum_latitudes-=most_left_event.latitude
            sum_longitudes-=most_left_event.longitude
            neighboors_size-=1

        left_index+=1
        right_index+=1

        if (right_index<trace_size) :
            most_right_event=trace[right_index]
            sum_latitudes+=most_right_event.latitude
            sum_longitudes+=most_right_event.longitude
            neighboors_size+=1
        
        event=Event(trace[i].datetime,sum_latitudes/neighboors_size,sum_longitudes/neighboors_size)
        filtered_trace.append(event)
              
    return filtered_trace

def _base_mean_filter_by_time(trace,kernel_shape) :
    """
    Perform a mean filter on the trace

    Parameters
    ----------
    trace : Trace
        A Trace object (see Trace in Model)

    kernel_shape : 2-tuple 
        the kernel_shape is 2-tuple (l,r) where l<=0 and r>=0 (in seconds),
        thus, when the filter estimate the position of an event which date
        time is 't', it will use all the events whcih datetime is in interval
        [t+l,t+r]

    Returns
    -------
    filtered_trace : Trace
        the filtered trace.

    Notes
    -----
    The commputational complexity is O(n)
    """
    
    trace_size=len(trace)
    filtered_trace=[]
    
    left_time_limit,right_time_limit=kernel_shape
    left_index,right_index=0,0
    current_event=most_left_event=trace[0]

    sum_latitudes,sum_longitudes=0,0
    neighboors_size=0
    while right_index<trace_size :
        to_test_event_right=trace[right_index]
        if (to_test_event_right.time_difference(current_event)<=right_time_limit) :
            most_right_event=to_test_event_right
            sum_latitudes+=most_right_event.latitude
            sum_longitudes+=most_right_event.longitude
            neighboors_size+=1
            right_index+=1
        else : break
        
    event=Event(most_left_event.datetime,sum_latitudes/neighboors_size,sum_longitudes/neighboors_size)
    filtered_trace.append(event)

    for i in xrange(1,trace_size) :
        current_event=trace[i]

        while left_index<trace_size :
            most_left_event=trace[left_index]
            if (most_left_event.time_difference(current_event)<left_time_limit) :
                sum_latitudes-=most_left_event.latitude
                sum_longitudes-=most_left_event.longitude
                neighboors_size-=1
                left_index+=1
            else : break
        
        while right_index<trace_size :
            to_test_event_right=trace[right_index]
            if (to_test_event_right.time_difference(current_event)<=right_time_limit) :
                most_right_event=to_test_event_right
                sum_latitudes+=most_right_event.latitude
                sum_longitudes+=most_right_event.longitude
                neighboors_size+=1
                right_index+=1
            else : break

        event=Event(trace[i].datetime,sum_latitudes/neighboors_size,sum_longitudes/neighboors_size)
        filtered_trace.append(event)
              
    return filtered_trace


class Mean_filter :
    """
    Perform a mean filter on the trace.

    Parameters
    ----------
    window_size : int, optional
        precise the size of the window used for filtering depends on neighbooring_type parameter
        if neighbooring_type='number' the window_size will precise the approximate number of event
        used; if neighbooring_type='time' the window_size will precise the size of window in seconds 

    window_type : {'causal', 'centered'}, optional
        'causal' : the filter is causal, thus, it use only actual and past events for each event
        'centered' : the filter is not causal, thus, it use past and futur events for each event

    neighbooring_type : {'number', 'time'}, optional
        the neighbooring_type change the signification of the window size, wether the neighbooring is
        calculated by time or just by order

    Attributes
    ----------
    filtered_trace_ : Trace
        the filtered trace.

    Notes
    -----
        - The commputational complexity is O(n)
        - The used distance is the euclidean distance.
    """

    def __init__(self,window_size=4,window_type='causal',neighbooring_type='number') :
        self.window_size=window_size
        self.window_type=window_type
        self.neighbooring_type=neighbooring_type

    def fit(self, trace) :
        """
        Perform a mean filter on the trace.

        Parameters
        ----------
        trace : Trace
            A Trace object (see Trace in Model)

        Returns
        -------
        filtered_trace_ : Trace
            the filtered trace.
        """

        self.filtered_trace_=_mean_filter(trace,window_size=self.window_size,window_type=self.window_type,neighbooring_type=self.neighbooring_type)
        return self.filtered_trace_
