import time
from library.model import Event,Trace
from library.visualization.visualize_trace import plot_trace_2D,plot_trace_3D
from library.data_management.csv_trace_reader import read_trace_from_CSV
from library.kdd.preprocessing.cleaning import *
from library.kdd.preprocessing.compression import *
from library.kdd.preprocessing.segmentation import *
from library.kdd.mining.poi_detection import *
import datetime

def get_synthetic_trace() :
    event1=Event(datetime.datetime(2015,1,1,10,0,0),10,1)
    event2=Event(datetime.datetime(2015,1,1,10,0,2),11,1)
    event3=Event(datetime.datetime(2015,1,1,10,0,4),19,1)
    event4=Event(datetime.datetime(2015,1,1,10,0,6),13,1)
    event5=Event(datetime.datetime(2015,1,1,10,0,8),14,1)
    trace=Trace()
    trace.add_events(event1,event2,event3,event4,event5)
    return trace

def get_real_trace(csv_source_file) :
    return read_trace_from_CSV(csv_source_file)

def just_try() :
    trace=get_synthetic_trace()
    SP=Stay_points(0.0001,1800)
    ST=Segmentation_by_time(1800)
    RDPC=RDP_compression(0.0001)
    MEANF=Mean_filter(10,'causal','number')
    MEDIANF=Median_filter(10,'causal','number','complete',epsilon=0.0001)
    
    starting_time=time.time()
    result_trace=MEANF.fit(trace)
    result_trace_2=MEDIANF.fit(trace)
    elapsed_time=time.time()-starting_time
    print "Elapsed time :",elapsed_time,"s"

    plot_trace_2D(trace,result_trace,result_trace_2)
    plot_trace_3D(trace,result_trace,result_trace_2)

just_try()
