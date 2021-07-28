import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm

m = 1.0 # mass
b = 1.0 # damping coeff
k = 10.0 # spring stiffness
f = 1.0 # force response on the damping system
dt = 0.1 # time steps we will take to simulate the system
time = 0.0 # we will take care of the simulation loop here

# we will follow the methodology of xk = Fxk-1 + Guk-1 where
# F = e^Adt and G = F[I - e^(-Adt)]A^(-1)B
# so then we will define matrix A and B since they will remain constant

A = np.array([[-b/m, -k/m],[1.0, 0.0]])
B = np.array([f*(1/m), 0.0])
F = expm(np.multiply(A,dt))
G = np.matmul(np.matmul(F,np.substract(np.identity(2),expm(np.multiply(A,-1*dt)))),np.matmul(np.linalg.inv(A),B))
Mat_tPlus1 = np.array([0.0,0.0]) #this will store the value of vDot at 0 and xDot at 1 for the next step.
Mat = np.array([0.0,0.0]) #this will store the value of veclocity at 0 and position at 1 for the next step. Initially we are assuming it 0
ansVelo, ansPos, timeList = [0], [0], [0] #initiating three empty list to populte later on

#running the loop untill we reach time interval of 10 sec with dt of 0.01 sec
while (time < 10):
    Mat_tPlus1 = np.matmul(F,Mat) + np.multiply(G,f)  #performing xDot(t) = Ax(t) + Bu(t) for the main equation
    Mat[0] += Mat_tPlus1[0]*dt #calculating velocity using acceleration 
    Mat[1] += Mat_tPlus1[1]*dt #calculating position using velocity
    time += dt #accumulating time as we go
    ansVelo.append(Mat[0]) # populating main three lists to plot the graph
    ansPos.append(Mat[1])
    timeList.append(time)

if (len(timeList) == len(ansVelo) and len(ansVelo) == len(ansPos)): #checking if the length of the lists are same
    fig, axis = plt.subplots(2,1) #creating two subplots to stack on eachother
    fig.suptitle('Euler 1st Order Damping Simulation')
    axis[0].plot(timeList,ansPos)
    axis[1].plot(timeList,ansVelo)
    # Hide x labels and tick labels for top plots and y ticks for right plots.
    axis[0].set(ylabel = 'Position (m)')
    axis[1].set(xlabel = 'Time(s)', ylabel = 'Velocity (m/s)')
    # Turning on grid for both graphs
    axis[0].grid(True)
    axis[1].grid(True)
    # Adding labels to the left of plots and at the bottom
    for ax in axis.flat:
        ax.label_outer()
    plt.show()
else:
    print("Length of all three lists is not equal!")
    print("Length of Time stamp list : {}".format(len(timeList)))
    print("Length of Velocity stamp list : {}".format(len(ansVelo)))
    print("Length of Position stamp list : {}".format(len(ansPos)))