from library.model import Event,Trace
from library.visualization.visualize_trace import plot_trace_2D,plot_trace_3D
from library.data_management.csv_trace_reader import read_trace_from_CSV
from library.kdd.preprocessing.cleaning.mean_filter import *
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
filtered_trace=mean_filter(trace,4,'causal','number')
plot_trace_3D(filtered_trace)

#for event in trace : print event
#filtered_trace=mean_filter(trace,4,'causal','time')
#filtered_trace=mean_filter(trace,5,'centered')
#print len(trace),"->",len(filtered_trace)
#for event in filtered_trace : print event
