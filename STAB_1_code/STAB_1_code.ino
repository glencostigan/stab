#include <SD.h> //Load the SD library
#include <SPI.h> //Load the SPI comm library

int chipSelect=4; //Set chipselct = 4
File mySensorData; //Variable for working with our file object

#include "Wire.h"    // imports the wire library for talking over I2C 
#include "Adafruit_BMP085.h"  // import the Pressure Sensor Library
Adafruit_BMP085 mySensor;  // create sensor object called mySensor

float tempC;  // Variable for holding temp in C
float tempF;  // Variable for holding temp in F
float pressure; //Variable for holding pressure reading

#include "I2Cdev.h" // import I2Cdev library required for MPU6050 library
#include "MPU6050.h" // import MPU6050 accel/gyro 6DOF sensor library
MPU6050 accelgyro; //create sensor object called accelgyro
int16_t ax, ay, az; //Variables for accel x-dir, y-dir, and z-dir
int16_t gx, gy, gz; //Variables for gyro x-dir, y-dir, and z-dir
#define OUTPUT_READABLE_ACCELGYRO //Output data as readable data

#include <HMC5883L.h> //import library for HMC5883L magnetometer (NEEDS 'Wire' library)
HMC5883L compass; //create sensor object called compass

#include <Servo.h> //import Servo library
Servo myservo; //create servo object called myservo

unsigned long time; //include time variable

void setup(){
pinMode(8, OUTPUT);
digitalWrite(8, HIGH);

//Serial.begin(9600); //turn on serial monitor (Uncomment when not testing)
mySensor.begin();   //initialize mySensor

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE // join I2C bus (I2Cdev library doesn't do this automatically)
Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
Fastwire::setup(400, true);
#endif
accelgyro.initialize();

compass.begin(); // Initialize Initialize HMC5883L
compass.setRange(HMC5883L_RANGE_1_3GA); // Set measurement range
compass.setMeasurementMode(HMC5883L_CONTINOUS); // Set measurement mode
compass.setDataRate(HMC5883L_DATARATE_30HZ); // Set data rate
compass.setSamples(HMC5883L_SAMPLES_8); // Set number of samples averaged
compass.setOffset(0, 0); // Set calibration offset. See HMC5883L_calibration.ino

myservo.attach(9); //Pin 9 for servo 1 and 2 (share same output angles)

pinMode(10, OUTPUT); //Reserve 10 as an output (SD LIBRAY REQUIREMENT)
SD.begin (chipSelect); //Initialize the SD card with chipSelect connected to pin 4

pinMode(2, OUTPUT); //Loop check LED
}

void loop() {
time = millis(); // find current time since program began

//Temperature and Pressure
tempC = mySensor.readTemperature(); //  Read Temperature
tempF = tempC*1.8 + 32.; // Convert degrees C to F
pressure=mySensor.readPressure(); //Read Pressure

//Accel and Gyro
accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz); //read accel/gyro data

//Compass
Vector norm = compass.readNormalize();
float heading = atan2(norm.YAxis, norm.XAxis); // Calculate heading
// Set declination angle on your location and fix heading
// You can find your declination on: http://magnetic-declination.com/
// (+) Positive or (-) for negative
// For Bytom / Poland declination angle is 4'26E (positive)
// Formula: (deg + (min / 60.0)) / (180 / M_PI);
float declinationAngle = (4.0 + (26.0 / 60.0)) / (180 / M_PI);
heading += declinationAngle; 
if (heading < 0) // Correct for heading < 0deg and heading > 360deg
{
heading += 2 * PI;
}
if (heading > 2 * PI)
{
heading -= 2 * PI;
}
float headingDegrees = heading * 180/M_PI; // Convert to degrees

// Servo
float a = 60; //max angle of attack
float d = 90;
float x = headingDegrees; //floored headingDegrees
//float b = x % 180; //new range of repeated values from 0 to 179. (alpha(theta=0) = aplha(theta=180))
float b = x; //adjusted heading
if (x > 180 && x <= 360){
  b = x - 180;
}
float c; //output angle of attack
if (b >= 15 && b <= 90){
  c = -a*sin((PI/150)*x-PI/10) + d;
}
else if (b > 90 && b <= 165){
  c = a*cos((PI/150)*x-3*PI/5) + d;
}
//else if (b >= 95 && b <= 130){
//  c = a*sin((PI/70)*x-19*PI/14) + d; 
//}
//else if (b >= 140 && b <= 175){
//  c = -a*cos((PI/70)*x) + d;
//}
else{
c = d;
}
myservo.write(c); //write to servo 1 and 2

mySensorData= SD.open("Data2.txt", FILE_WRITE); //Open PTData.txt on the SD card as a file to write.

if (mySensorData) { //Only do these things if data file opened successfully
/*
Serial.print("The Temp is: "); //Print Your results of BMP180 data (Uncomment when not testing)
Serial.print(tempF); //(Uncomment when not testing)
Serial.println(" degrees F"); //(Uncomment when not testing)
Serial.print("The Pressure is: "); //(Uncomment when not testing)
Serial.print(pressure); //(Uncomment when not testing)
Serial.println(" Pa."); //(Uncomment when not testing)
Serial.println("");  //(Uncomment when not testing)

Serial.print("a/g:\t");  //Print results of MPU6050 data (Uncomment when not testing)
Serial.print(ax); Serial.print("\t");  //(Uncomment when not testing)
Serial.print(ay); Serial.print("\t");  //(Uncomment when not testing)
Serial.print(az); Serial.print("\t");  //(Uncomment when not testing)
Serial.print(gx); Serial.print("\t");  //(Uncomment when not testing)
Serial.print(gy); Serial.print("\t");  //(Uncomment when not testing)
Serial.println(gz);  //(Uncomment when not testing)
Serial.println("");  //(Uncomment when not testing)

Serial.print(" Heading = ");  //Print results of HMC5883L data (Uncomment when not testing)
Serial.print(heading);  //(Uncomment when not testing)
Serial.print(" Degress = ");  //(Uncomment when not testing)
Serial.print(headingDegrees);  //(Uncomment when not testing)
Serial.println("");  //(Uncomment when not testing)
*/

digitalWrite(2, HIGH); //Loop check LED on
delay(100); //Pause between readings.
digitalWrite(2, LOW); //Loop check LED off

mySensorData.print(time); //Write tempF to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(tempF); //Write tempF to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(pressure); //Write pressure data 
mySensorData.print(","); //Write comma to the line
mySensorData.print(ax); //Write ax to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(ay); //Write ay to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(az); //Write az to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(gx); //Write gx to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(gy); //Write gy to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(gz); //Write gz to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.print(heading); //Write heading to the SD card
mySensorData.print(","); //Write comma to the line
mySensorData.println(headingDegrees); //Write headingDegrees to the SD card and go to next line
mySensorData.close(); //Close the file
}
}
