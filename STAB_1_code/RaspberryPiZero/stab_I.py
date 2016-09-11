import time
import csv
import numpy

time = time.strftime("%H_%M_%S")
date = time.strftime("%Y_%m_%d")
filename = time + 'EST' + date + '_data' + '.csv'
c = csv.writer(open(filename), "wb"))

current_milli_time = lambda: int(round(time.time() * 1000))

########given#######
#state launch conditions
R = 287 #J/(kg*K)
h_o = 0 #m
P_o = 101300 #Pa
L = -0.0065 #K/m
T_o = 273 #K
g = 9.81 #m/s^2
#state the gain of motor
gain = 2
#initialize fin position
phi = 0 #degrees
servo(phi)
#state desired roll
r = 10 #degrees/s
#create initial .csv
#needs 0 for every column for the first row where t = 0.
c.writerow(["Time (ms)","del_t (ms)","Roll (Degrees)","Pitch (Degrees)", \
            "Yaw (Degrees)","Omega_X (Degrees/s)","Omega_Y (Degrees/s)", \
            "Omega_Z (Degrees/s)","Alpha_X (Degrees/s^2)", \
            "Alpha_Y (Degrees/s^2)","Alpha_Z (Degrees/s^2)", \
            "x (m)","y (m)","z (m)","u (m/s)", "v (m/s)", "w (m/s)", \
            "a_x (m/s^2)", "a_y (m/s^2)", "a_z (m/s^2)","Phi (Degrees)", \
            "Error (Degrees)","Pressure (Pa)","Temperature (K)", \
            "Density (kg/m)", "Height (m)"])
t = 0

var = 1
while var == 1 : #infinite loop
    #calculate time
        t_old = t
        t = current_milli_time()
        del_t = t - t_old
    #calcualte om_x, om_y, om_z angular velocities
        #read straight from MPU-6050 gyroscope
        om_x =
        om_y =
        om_z =
    #calculate roll, pitch, yaw angular positions
        roll = om_x*del_t
        pitch = om_y*del_t
        yaw = om_z*del_t
    #calcualte al_x, al_y, al_z angular accelerations
        al_x = om_x/del_t
        al_y = om_y/del_t
        al_z = om_z/del_t
    #calcualte a_x, a_y, a_z accelerations
        #read straight from ADXL377 high-g accelerometer
        a_x =
        a_y =
        a_z =
    #calculate x, y, z position
        x = a_x/(del_t)^2
        y = a_y/(del_t)^2
        z = a_z/(del_t)^2
    #calculate u, v, w velocities
        u = a_x/del_t
        v = a_y/del_t
        w = a_z/del_t
    #calculate P, T, h, rho
        #read from BMP180 sensor
        P =
        T =
        rho = P/(R*T)
        h = (T/L)*((P_o/P)^(R*L/g)-1)+h_o
    #calculate error
    error = r - roll
    #apply the controlled gain to the servo based on the error
    phi = gain*error
    #write out to .csv file
    c.writerow([t,del_t,roll,pitch,yaw,om_x,om_y,om_z,al_x,al_y,al_z,x,y,z, \
                u,v,w,a_x,a_y,a_z,phi,error,P,T,rho,h])
    #delay to protect code from breaking.
    time.sleep(0.010) #seconds
