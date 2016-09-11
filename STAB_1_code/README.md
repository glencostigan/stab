# Raspberry Pi Zero Config: MPU 6050

Reference:

http://blog.bitify.co.uk/2013/11/interfacing-raspberry-pi-and-mpu-6050.html

http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html

# Setup i2c (Raspbian Jessie)
```
# nano /etc/modules
```
Add the following lines:

```
# i2c-bcm2708
# i2c-dev
```

Connect MPU-6050 to i2c connections

![RaspberryPiZeroPinout](https://elementztechblog.files.wordpress.com/2016/05/gpio.png?w=700)

```
Pin 2 - 5V connect to VCC
Pin 3 - SDA connect to SDA
Pin 5 - SCL connect to SCL
Pin 6 - Ground connect to GND
```

Check if MPU-6050 is connected.
	# apt-get install i2c-tools
	# i2cdetect -y 1


You should see this output:
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
Enter the following command and you should get an output of 0x68 on screen if everything is working properly.
	# i2cget -y 1 0x68 0x75
This command talks to the device whose address is 0x68 (the sensor) and retrieves the value in the register 0x75 which has a default value of 0x68 the same value as the address.
READING FROM PYTHON
Download smbus module for python
# apt-get install python-smbus
Use the following test code for reading the sensor with python:

#!/usr/bin/python

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

print "gyro data"
print "---------"

gyro_xout = read_word_2c(0x43)
gyro_yout = read_word_2c(0x45)
gyro_zout = read_word_2c(0x47)

print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

print
print "accelerometer data"
print "------------------"

accel_xout = read_word_2c(0x3b)
accel_yout = read_word_2c(0x3d)
accel_zout = read_word_2c(0x3f)

accel_xout_scaled = accel_xout / 16384.0
accel_yout_scaled = accel_yout / 16384.0
accel_zout_scaled = accel_zout / 16384.0

print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

Run the code (run it twice if no real data the first time)
	# python /python/MPU-6050/testsensor.py
Output should look something like this:
gyro data
---------
gyro_xout:  -92  scaled:  -1
gyro_yout:  294  scaled:  2
gyro_zout:  -104 scaled:  -1

accelerometer data
------------------
accel_xout:  -3772  scaled:  -0.230224609375
accel_yout:  -52    scaled:  -0.003173828125
accel_zout:  15408  scaled:  0.9404296875
x rotation:  -13.7558411667
y rotation:  -0.187818934829
Refer to reference for more clarification on code and math involved.

HMC5883L
Reference: http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html

Setup i2c (Raspbian Jessie)
	# nano /etc/modules
Add the following lines:
	# i2c-bcm2708
# i2c-dev
Connect HMC5883L to i2c connections

Pin 1 - 5V connect to VCC
Pin 3 - SDA connect to SDA
Pin 5 - SCL connect to SCL
Pin 6 - Ground connect to GND
Check if HMC5883L is connected.
	# apt-get install i2c-tools
	# i2cdetect -y 1
You should see this output:
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1e --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
PYTHON
Run /python/HMC5883L/findoffset.py
Output:
		minx:  -149
miny:  -368
maxx:  237
maxy:  65
x offset:  44
y offset:  -152
Use the x and y offset found and change it in /python/HMC5883L/testsensor.py
Run /python/HMC5883L/testsensor.py and test every 90 degrees.
