import time
import csv
import numpy
import Adafruit_BMP.BMP085 as BMP180
import Adafruit_ADS1x15.ADS1115 as adc
import smbus

power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(0)
address = 0x1e

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

def set(property, value):
    try:
        f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
        f.write(value)
        f.close()
    except:
        print("Error writing to: " + property + " value: " + value)

def current_milli_time():
    return lambda: int(round(time.time() * 1000))

def setServo(angle):
    set("servo", str(angle))

def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def write_to_csv(var):
    time_current = time.strftime("%H_%M_%S")
    date = time.strftime("%Y_%m_%d")
    filename = time_current + "EST" + date + "_data" + ".csv"
    with open(filename, "wb") as fb:
        c = csv.writer(fb)
        c.writerow(var)

def main():
    set("delayed", "0")
    set("mode", "servo")
    set("servo_max", "180")
    set("active", "1")

    delay_period = 0.01
    t = 0
    var = 1
    scale = 200

    ########given#######
    # state launch conditions
    R = 287  # J/(kg*K)
    # h_o = 0  # m
    # P_o = 101300  # Pa
    # L = -0.0065  # K/m
    # T_o = 273  # K
    # g = 9.81  # m/s^2
    # state the gain of motor
    kp = 2
    ki = 0
    kd = 1
    # initialize fin position
    phi = 0  # degrees
    setServo(phi)
    # state desired roll
    r = 10  # degrees/s

    while True:  # infinite loop
        # calculate time
        t_old = t
        t = current_milli_time()
        del_t = t - t_old
        # calcualte om_x, om_y, om_z angular velocities
        # read straight from MPU-6050 gyroscope (scaled)
        om_x = read_word_2c(0x43) / 131
        om_y = read_word_2c(0x45) / 131
        om_z = read_word_2c(0x47) / 131
        # calculate roll, pitch, yaw angular positions
        roll = om_x * del_t
        pitch = om_y * del_t
        yaw = om_z * del_t
        # calcualte al_x, al_y, al_z angular accelerations
        al_x = om_x / del_t
        al_y = om_y / del_t
        al_z = om_z / del_t
        # calcualte a_x, a_y, a_z accelerations
        # read straight from ADXL377 high-g accelerometer
        a_x = arduino_map(adc.read_adc(0), 0, 675, -scale, scale)
        a_y = arduino_map(adc.read_adc(1), 0, 675, -scale, scale)
        a_z = arduino_map(adc.read_adc(2), 0, 675, -scale, scale)
        # calculate x, y, z position
        x = a_x / (del_t) ^ 2
        y = a_y / (del_t) ^ 2
        z = a_z / (del_t) ^ 2
        # calculate u, v, w velocities
        u = a_x / del_t
        v = a_y / del_t
        w = a_z / del_t
        # calculate P, T, h, rho
        # read from BMP180 sensor
        P = BMP180.read_pressure()
        P_o = BMP180.read_sealevel_pressure()
        T = BMP180.read_temperature()
        rho = P / (R * T)
        h = BMP180.read_altitude()
        # h = (T/L)*((P_o/P)^(R*L/g)-1)+h_o
        # calculate error
        e = r - roll
        e_int = e * t
        e_der = e / del_t
        # apply the controlled gain to the servo based on the error
        phi = kp * e + ki * e_int + kd * e_der
        setServo(phi)
        time.sleep(delay_period)
        var = [t, del_t, roll, pitch, yaw, om_x, om_y, om_z, al_x, al_y, al_z, x, y, z,
            u, v, w, a_x, a_y, a_z, phi, e, P, T, rho, h]
        write_to_csv(var)
        # write out to .csv file
        # delay to protect code from breaking.
        time.sleep(0.010)  # seconds

if __name__ == '__main__':
    main()
