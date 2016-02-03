"""
Median Filter
"""

#Author : Belfodil Aimene <aimene.belfodil@insa-lyon.fr>

from ....model import Event


def median_filter(trace,window_size=4,window_type='causal',neighbooring_type='number') :
    """
    Perform a mean filter on the trace

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
    The computational complexity is O(n)
    """
    
    if (window_type=='causal') : kernel_shape=(-window_size,0)
    elif (window_type=='centered') : kernel_shape=(-(window_size/2),window_size/2)
    else : raise Exception("window_type dosen't exists")

    if (neighbooring_type=='number') : filtered_trace=_base_median_filter(trace,kernel_shape)
    elif (neighbooring_type=='time') : filtered_trace=_base_median_filter_by_time(trace,kernel_shape)
    else : raise Exception("neighbooring_type dosen't exists")

    return filtered_trace


def _get_median(points_list) :
    """
    """
    return points_list[0] 

def _base_median_filter(trace,kernel_shape) :
    """
    Perform a median filter on the trace

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
    The computational complexity is O(n)
    """
    
    trace_size=len(trace)
    filtered_trace=[]
    
    left_index,right_index=kernel_shape

    neighboors=[(position.latitude,position.longitude) for position in trace[0:right_index+1]]
    median_latitude,median_longitude=_get_median(neighboors)
    event=Event(trace[0].datetime,median_latitude,median_longitude)
    filtered_trace.append(event)

    for i in xrange(1,trace_size) :

        if (left_index>=0) :
            neighboors.pop(0)

        left_index+=1
        right_index+=1

        if (right_index<trace_size) :
            most_right_event=trace[right_index]
            neighboors.append((most_right_event.latitude,most_right_event.longitude))

        median_latitude,median_longitude=_get_median(neighboors)
        event=Event(trace[i].datetime,median_latitude,median_longitude)
        filtered_trace.append(event)
              
    return filtered_trace

def _base_median_filter_by_time(trace,kernel_shape) :
    """
    Perform a median filter on the trace

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
    The computational complexity is O(n)
    """
    
    trace_size=len(trace)
    filtered_trace=[]
    
    left_time_limit,right_time_limit=kernel_shape
    left_index,right_index=0,0
    current_event=trace[0]
    neighboors=[]
    
    while right_index<trace_size :
        new_event=trace[right_index]
        if (new_event.time_difference(current_event)<=right_time_limit) :
           neighboors.append((new_event.latitude,new_event.longitude))
           right_index+=1
        else : break

    median_latitude,median_longitude=_get_median(neighboors)
    event=Event(trace[0].datetime,median_latitude,median_longitude)
    filtered_trace.append(event)

    for i in xrange(1,trace_size) :
        current_event=trace[i]

        while left_index<trace_size :
            past_event=trace[left_index]
            if (past_event.time_difference(current_event)<left_time_limit) :
                neighboors.pop(0)
                left_index+=1
            else : break
        
        while right_index<trace_size :
            new_event=trace[right_index]
            if (new_event.time_difference(current_event)<=right_time_limit) :
               neighboors.append((new_event.latitude,new_event.longitude))
               right_index+=1
            else : break

        median_latitude,median_longitude=_get_median(neighboors)
        event=Event(trace[0].datetime,median_latitude,median_longitude)
        filtered_trace.append(event)
              
    return filtered_trace
