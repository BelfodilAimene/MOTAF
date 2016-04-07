import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import cycle

def plot_trace_2D(*traces) :
    plt.figure(1)
    plt.clf()
    colors=cycle('bgrcmy')
    for trace,color in zip(traces,colors) :
        latitudes,longitudes=zip(*[(event.latitude,event.longitude) for event in trace])
        plt.plot(longitudes,latitudes, 'o-',color=color)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

def plot_trace_3D(*traces) :
    fig=plt.figure(1)
    plt.clf()
    colors=cycle('bgrcmy')
    first_event=None
    
    for trace in traces :
        if (not first_event) : first_event=trace[0]
        elif (first_event.time_difference(trace[0])>0) : first_event=trace[0] 
        
    for trace,color in zip(traces,colors) :
        latitudes,longitudes,time_dimension=[],[],[]
        for event in trace :
            latitudes.append(event.latitude)
            longitudes.append(event.longitude)
            time_dimension.append(event.time_difference(first_event))
        ax = fig.gca(projection='3d')
        ax.plot(longitudes, latitudes , time_dimension,'o-',color=color)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Time')
    plt.show()
    
