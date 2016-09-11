# HMC5883L
Reference: http://blog.bitify.co.uk/2013/11/connecting-and-calibrating-hmc5883l.html

Setup i2c (Raspbian Jessie)
```
# nano /etc/modules
```
Add the following lines:
```
i2c-bcm2708
i2c-dev
```
Connect HMC5883L to i2c connections
![RaspberryPiZeroPinout](https://elementztechblog.files.wordpress.com/2016/05/gpio.png?w=700)

```
Pin 2 - 5V connect to VCC
Pin 3 - SDA connect to SDA
Pin 5 - SCL connect to SCL
Pin 6 - Ground connect to GND
```
Check if HMC5883L is connected.
```
# apt-get install i2c-tools
# i2cdetect -y 1
```
You should see this output:
```
Output:
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- 1e --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
# PYTHON
Run `/python/HMC5883L/findoffset.py`

Output:
```
minx:  -149
miny:  -368
maxx:  237
maxy:  65
x offset:  44
y offset:  -152
```
Use the x and y offset found and change it in `/python/HMC5883L/testsensor.py`

Run `/python/HMC5883L/testsensor.py` and test every 90 degrees.
