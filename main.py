import time
from library.model import Event,Trace
from library.visualization.visualize_trace import plot_trace_2D,plot_trace_3D
from library.data_management.csv_trace_reader import read_trace_from_CSV
from library.kdd.preprocessing.cleaning import *
from library.kdd.preprocessing.compression import *
from library.kdd.preprocessing.segmentation import *
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

def get_real_trace(csv_source_file="../Data Samples/280.csv") :
    return read_trace_from_CSV("../Data Samples/280.csv")

trace=get_real_trace()
#segmented=segment_by_time(trace)
#compressed=rdp_compress(trace)
#plot_trace_2D(trace,compressed)
#plot_trace_3D(trace,compressed)

#for event in trace : print event
print "Filtering ..."
#filtered_trace=median_filter(trace,4,'causal','time') #,epsilon=0.000001
starting_time=time.time()
filtered_trace=median_filter(trace,10,'causal','number','weiszfeld',epsilon=0.1)
elapsed_time=time.time()-starting_time
print elapsed_time
#for event in filtered_trace : print event
plot_trace_2D(trace,filtered_trace)
