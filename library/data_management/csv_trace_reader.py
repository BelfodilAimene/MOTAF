from pandas import read_csv
from dateutil import parser
from ..model import Trace,Event

def read_trace_from_CSV(csv_file) :
    data=read_csv(filepath_or_buffer=csv_file,delimiter=';',encoding='utf-8')
    values=data[["recorded_at","latitude","longitude"]].values
    trace=Trace()
    for value in values :
        trace.add_event(Event(parser.parse(value[0]),value[1],value[2]))
    return trace
