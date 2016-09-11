import time

current_milli_time = lambda: int(round(time.time() * 1000))

########given#######
#state the gain of motor
gain = 2
#initialize fin position
phi = 0 #degrees
servo(phi)
#state desired roll
r = 10 #degrees/s
#create initial .csv
#needs 0 for every column for the first row where t = 0.
t = 0

########loop########
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
#write out to .csv file

#calculate error
error = r - roll
#apply the controlled gain to the servo based on the error
phi = gain*error
#delay to protect code from breaking.
delay(50)
#####endloop######
