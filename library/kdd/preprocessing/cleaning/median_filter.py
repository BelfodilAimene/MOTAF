"""
Median Filter
"""

#Author : Belfodil Aimene <aimene.belfodil@insa-lyon.fr>

import math
from ....model import Event,Position

def median_filter(trace,window_size=4,window_type='causal',neighbooring_type='number',algorithm='weiszfeld',**kwargs) :
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

    algorithm : {'weiszfeld','complete'}, optional
        the used algorithme to calculate median for a list of 2D-points
        'weiszfeld' : the iterative algorithme of Weiszdeld corrected by Yehuda Vardi and Cun-Hui Zhang
            in the paper "The multivariate L1-median and associated data depth, 1999", the median point
            is don't necessarily chosen from the given list of points, it return the geometric median   
        'complete' : an exact method which return the point which minimize the sum of distance with
            the other points in the given list of points. This method has more computation complexity
            relatively to weiszfeld algorithme

    kwargs :
        epsilon : float, optional
            used only when the used algorithm=weiszfeld, it precise the convergence criteria (i.e.
            the distance between the point and its next in the iterative algorithm is smaller than epsilon)
            the used default value is 0.00001

    Returns
    -------
    filtered_trace : Trace
        the filtered trace.

    """
    
    if (window_type=='causal') : kernel_shape=(-window_size,0)
    elif (window_type=='centered') : kernel_shape=(-(window_size/2),window_size/2)
    else : raise Exception("window_type dosen't exists")

    if (neighbooring_type=='number') : filtered_trace=_base_median_filter(trace,kernel_shape,algorithm,**kwargs)
    elif (neighbooring_type=='time') : filtered_trace=_base_median_filter_by_time(trace,kernel_shape,algorithm,**kwargs)
    else : raise Exception("neighbooring_type dosen't exists")

    return filtered_trace

def _base_median_filter(trace,kernel_shape,algorithm,**kwargs) :
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

    algorithm : {'weiszfeld','complete'}, optional
        the used algorithme to calculate median for a list of 2D-points
        'weiszfeld' : the iterative algorithme of Weiszdeld corrected by Yehuda Vardi and Cun-Hui Zhang
            in the paper "The multivariate L1-median and associated data depth, 1999", the median point
            is don't necessarily chosen from the given list of points, it return the geometric median   
        'complete' : an exact method which return the point which minimize the sum of distance with
            the other points in the given list of points. This method has more computation complexity
            relatively to weiszfeld algorithme

    kwargs :
        epsilon : float, optional
            used only when the used algorithm=weiszfeld, it precise the convergence criteria (i.e.
            the distance between the point and its next in the iterative algorithm is smaller than epsilon)
            the used default value is 0.00001

    Returns
    -------
    filtered_trace : Trace
        the filtered trace.
    """
    
    if (algorithm=='weiszfeld') :
        _get_median=_get_median_weiszfeld
        if (not kwargs.has_key('epsion')) :
            kwargs['epsilon']=0.00001
    elif (algorithm=='complete') :
        _get_median=_get_median_complete
    else : raise Exception("algorithm dosen't exists")
    
    trace_size=len(trace)
    filtered_trace=[]
    
    left_index,right_index=kernel_shape

    neighboors=trace[0:right_index+1]
    median_position=_get_median(neighboors,**kwargs)
    event=Event(trace[0].datetime,median_position.latitude,median_position.longitude)
    filtered_trace.append(event)

    for i in xrange(1,trace_size) :

        if (left_index>=0) :
            neighboors.pop(0)

        left_index+=1
        right_index+=1

        if (right_index<trace_size) :
            neighboors.append(trace[right_index])
        median_position=_get_median(neighboors,**kwargs)
        event=Event(trace[i].datetime,median_position.latitude,median_position.longitude)
        filtered_trace.append(event)
              
    return filtered_trace

def _base_median_filter_by_time(trace,kernel_shape,algorithm,**kwargs) :
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

    algorithm : {'weiszfeld','complete'}, optional
        the used algorithme to calculate median for a list of 2D-points
        'weiszfeld' : the iterative algorithme of Weiszdeld corrected by Yehuda Vardi and Cun-Hui Zhang
            in the paper "The multivariate L1-median and associated data depth, 1999", the median point
            is don't necessarily chosen from the given list of points, it return the geometric median   
        'complete' : an exact method which return the point which minimize the sum of distance with
            the other points in the given list of points. This method has more computation complexity
            relatively to weiszfeld algorithme

    kwargs :
        epsilon : float, optional
            used only when the used algorithm=weiszfeld, it precise the convergence criteria (i.e.
            the distance between the point and its next in the iterative algorithm is smaller than epsilon)
            the used default value is 0.00001

    Returns
    -------
    filtered_trace : Trace
        the filtered trace.
    """

    if (algorithm=='weiszfeld') :
        _get_median=_get_median_weiszfeld
        if (not kwargs.has_key('epsion')) :
            kwargs['epsilon']=0.00001
    elif (algorithm=='complete') :
        _get_median=_get_median_complete
    else : raise Exception("algorithm dosen't exists")
        
    trace_size=len(trace)
    filtered_trace=[]
    
    left_time_limit,right_time_limit=kernel_shape
    left_index,right_index=0,0
    current_event=trace[0]
    neighboors=[]
    
    while right_index<trace_size :
        new_event=trace[right_index]
        if (new_event.time_difference(current_event)<=right_time_limit) :
           neighboors.append(new_event)
           right_index+=1
        else : break
        
    median_position=_get_median(neighboors,**kwargs)
    event=Event(trace[0].datetime,median_position.latitude,median_position.longitude)
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
               neighboors.append(new_event)
               right_index+=1
            else : break
        median_position=_get_median(neighboors,**kwargs)
        event=Event(trace[i].datetime,median_position.latitude,median_position.longitude)
        filtered_trace.append(event)
              
    return filtered_trace

def _get_median_complete(points_list,**kwargs) :
    """
    It's an exact method which return the point which minimize the sum of distance with
    the other points in the given list of points. This method has more computation complexity
    relatively to weiszfeld iterative algorithme.

    Parameters
    ----------
    points_list : list<Position>
        A list of Position object (see Position in Model)
        
    kwargs is not used
    -------
    median_point : Position
        the geometric median position.
    """
    
    sum_distances=[0]*len(points_list)

    point_index=0
    for point in points_list :
        for point_2 in points_list :
            sum_distances[point_index]+=point.euclidean_distance(point_2)
        point_index+=1
    median_point=min(zip(sum_distances,points_list),key = lambda element : element[0])[1]
    return median_point

def _get_median_weiszfeld(points_list,epsilon) :
    """
    It's an iterative algorithme of Weiszdeld corrected by Yehuda Vardi and Cun-Hui Zhang
    in the paper "The multivariate L1-median and associated data depth, 1999", the returned
    geometric median isn't necessarily chosen from the given list of points.
    The used initial point is the mean point of the points_list.

    Parameters
    ----------
    points_list : list<Position>
        A list of Position object (see Position in Model)

    epsilon : float 
        it precise the convergence criteria (i.e. the distance between the point and its next in
        the iterative algorithm is smaller than epsilon)

    Returns
    -------
    median_point : Position
        the geometric median position.
    """
    sum_distances=[0]*len(points_list)
    initial_point_latitude,initial_point_longitude=0,0
    for point in points_list :
        initial_point_latitude+=point.latitude
        initial_point_longitude+=point.longitude
    
    last_point=initial_point=Position(initial_point_latitude/len(points_list),initial_point_longitude/len(points_list))
    new_point=_get_next_weiszfeld_point(points_list,last_point)

    while (new_point.euclidean_distance(last_point)>epsilon) :
        last_point=new_point
        new_point=_get_next_weiszfeld_point(points_list,last_point)

    median_point=new_point
    return median_point 

def _get_next_weiszfeld_point(points_list,last_point) :
    """
    Get the next point in the weiszfeld iterative algorithme for median point
    calculus where the last point if last_point and the point list is points_list.  

    Parameters
    ----------
    points_list : list<Position>
        A list of Position object (see Position in Model)

    last_point : Position 
        the last median point (iterative method)

    Returns
    -------
    next_point : Position
        the new median point  (iterative method)
    """
    new_point_latitude_non_equal,new_point_longitude_non_equal=0,0
    last_point_latitude,last_point_longitude=last_point.latitude,last_point.longitude

    last_point_in_points_list=False
    last_point_centralized_latitude,last_point_centralized_longitude=0,0

    weights_sum=0
    
    for point in points_list :
        distance=point.euclidean_distance(last_point)
        if (distance>0) :
            weight=1/distance
            weights_sum+=weight
            new_point_latitude_non_equal+=weight*point.latitude
            new_point_longitude_non_equal+=weight*point.longitude
            last_point_centralized_latitude+=weight*(point.latitude-last_point_latitude)
            last_point_centralized_longitude+=weight*(point.longitude-last_point_longitude)
        else :
            last_point_in_points_list=True
            
    if (weights_sum==0) :
        new_point=last_point
    else :
        new_point_latitude_non_equal/=weights_sum
        new_point_longitude_non_equal/=weights_sum
        if (not last_point_in_points_list) :
            new_point=Position(new_point_latitude_non_equal,new_point_longitude_non_equal)
        else :
            last_point_centralized_latitude/=weights_sum
            last_point_centralized_longitude/=weights_sum
            last_point_centralized_module=math.sqrt(last_point_centralized_latitude*last_point_centralized_latitude+last_point_centralized_longitude*last_point_centralized_longitude)
            last_point_weight=min(1,1/last_point_centralized_module) if (last_point_centralized_module>0) else 1
            new_point_latitude=(1-last_point_weight)*new_point_latitude_non_equal+last_point_weight*last_point_latitude
            new_point_longitude=(1-last_point_weight)*new_point_longitude_non_equal+last_point_weight*last_point_longitude            
            new_point=Position(new_point_latitude,new_point_longitude)
    return new_point
