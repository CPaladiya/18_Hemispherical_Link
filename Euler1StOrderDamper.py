import numpy as np
import matplotlib.pyplot as plt

m = 1.0 # mass
b = 1.0 # damping coeff
k = 10.0 # spring stiffness
f = 1.0 # force response on the damping system
dt = 0.01 # time steps we will take to simulate the system
time = 0.0 # we will take care of the simulation loop here

# we will follow the methodology of xDot(t) = Ax(t) + Bu(t)
# so then we will define matrix A and B since they will remain constant

A = np.array([[-b/m, -k/m],[1.0, 0.0]])
print(A)
B = np.array([f*(1/m), 0.0])
Mat_tPlus1 = np.array([0.0,0.0]) #this will store the value of vDot at 0 and xDot at 1 for the next step.
Mat = np.array([0.0,0.0]) #this will store the value of veclocity at 0 and position at 1 for the next step. Initially we are assuming it 0

#plt.plot(Mat[0],Mat[1],'ro')

if True:
    while (time < 10):
        Mat_tPlus1 = np.matmul(A,Mat) + B
        print("Mat Plust t {}".format(Mat_tPlus1))
        print("Mat {}".format(Mat))
        Mat[0] += Mat_tPlus1[0]*dt
        Mat[1] += Mat_tPlus1[1]*dt
        time += dt
        plt.plot(time,Mat[0],'ro')
        plt.plot(time,Mat[1],'bo')

plt.show()   
