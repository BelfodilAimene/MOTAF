import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_trace_2D(trace) :
    latitudes,longitudes=zip(*[(event.latitude,event.longitude) for event in trace])
    plt.figure(1)
    plt.clf()
    plt.plot(longitudes,latitudes, 'bo-')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title('Trace size : {0} event'.format(len(trace)))
    plt.show()

def plot_trace_3D(trace) :
    latitudes,longitudes,time_dimension=[],[],[]
    first_event=trace[0]
    for event in trace :
        latitudes.append(event.latitude)
        longitudes.append(event.longitude)
        time_dimension.append(event.time_difference(first_event))
    fig=plt.figure(1)
    ax = fig.gca(projection='3d')
    ax.plot(longitudes, latitudes , time_dimension,'bo-')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Time')
    plt.title('Trace size : {0}'.format(len(trace)))
    plt.show()
    
