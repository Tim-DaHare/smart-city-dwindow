# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bme680
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from datetime import datetime
# from PIL import ImageFont
import busio
import adafruit_sgp30
from luma.core.interface.serial import i2c
# from luma.core.render import canvas
from luma.oled.device import sh1106
import db as db
import random

#OLED
serial = i2c(port=1, address=0x3C)
# device = sh1106(serial)
# device.rotate = 0 #ligt aan je display, kan 0, 1, 2, 3 zijn

i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor object, communicating over the board's default I2C bus
# bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# factory = PiGPIOFactory()
# change this to match the location's pressure (hPa) at sea level
# bme680.sea_level_pressure = 1013.25
rgbPins = {'pinRed': 26, 'pinGreen': 19, 'pinBlue': 13}

#SGP30
i2cSGP = busio.I2C(board.SCL, board.SDA, frequency=100000)
# sgp30 = adafruit_sgp30.Adafruit_SGP30(i2cSGP)

#Baseline values: eCO2 = 0x8f87, TVOC = 0x8f55
# sgp30.iaq_init()
# sgp30.set_iaq_baseline(0x8973, 0x8AAE)
# sgp30.set_iaq_baseline(0x8f87, 0x8f55)

# Offset for temprature measurements in c
temperature_offset = -5

devices = i2c.scan()

oled_addr = 0x3c

# Tygo/prototype
L1 = 26
L2 = 19
L3 = 5 
L4 = 6 

C1 = 13
C2 = 22
C3 = 17
C4 = 27 

# GPIO.setmode(GPIO.BOARD)
# for i in rgbPins:
#     GPIO.setup(rgbPins[i], GPIO.OUT)
#     GPIO.setup(rgbPins[i], GPIO.HIGH)

# pinRed = GPIO.PWIM(rgbPins['pinRed'], 2000)
# pinGreen = GPIO.PWIM(rgbPins['pinGreen'], 2000)
# pinBlue = GPIO.PWIM(rgbPins['pinBlue'], 2000)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# red = 13
# green = 19
# blue = 26

#LED RGB
#GPIO.setup(red, GPIO.OUT) #RED
#GPIO.setup(green, GPIO.OUT) #GREEN
#GPIO.setup(blue, GPIO.OUT) #BLUE

#Codepad
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#SERVO
# servo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000,pin_factory=factory)

# GPIO.output(red, GPIO.LOW)
# GPIO.output(green, GPIO.LOW)
# GPIO.output(blue, GPIO.LOW)

keyPadNumber = "1"
workingKeypadNumbers = ["1", "2", "3", "4"]

def openWindow():
    # servo.value = 0
    print("window open")
def closeWindow():
    # servo.value = 1
    print("window open")

# def setPinYellow():
#     GPIO.output(red, GPIO.LOW)
#     GPIO.output(green, GPIO.LOW)
#     GPIO.output(blue, GPIO.HIGH)
# def setPinRed():
#     GPIO.output(red, GPIO.LOW)
#     GPIO.output(green, GPIO.HIGH)
#     GPIO.output(blue, GPIO.HIGH)
# def setPinGreen():
#     GPIO.output(red, GPIO.HIGH)
#     GPIO.output(green, GPIO.LOW)
#     GPIO.output(blue, GPIO.HIGH)
# def setPinBlue():
#     GPIO.output(red, GPIO.HIGH)
#     GPIO.output(green, GPIO.HIGH)
#     GPIO.output(blue, GPIO.LOW)
# def setPinNeutral():
#     GPIO.output(red, GPIO.LOW)
#     GPIO.output(green, GPIO.LOW)
#     GPIO.output(blue, GPIO.LOW)

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    global keyPadNumber
    if(GPIO.input(C1) == 1):
        keyPadNumber = characters[0]
    if(GPIO.input(C2) == 1):
        keyPadNumber = characters[1]
    if(GPIO.input(C3) == 1):
        keyPadNumber = characters[2]
    if(GPIO.input(C4) == 1):
        keyPadNumber = characters[3]
    GPIO.output(line, GPIO.LOW)

def showLED(color):
    if color == 'green':
        print()

def measure_data():
    return 26.1, 30, 22

def shouldWindowOpen(celcius, eco2, tvoc):
    rand = random.random()
    return rand < 0.5
    
def main(delay = 0.5):
    conn = db.create_connection(r"sensor_dataset.db")

    # Db init
    if conn is None:
        raise Exception("connection could not be created")

    with conn:
        create_dr_q = """CREATE TABLE IF NOT EXISTS data_readings (id integer PRIMARY KEY, measured_at text, temprature real, eco2 integer, tvoc integer, window_open tinyint, is_raining tinyint); """
        db.create_table(conn, create_dr_q)

        create_vth_q = """CREATE TABLE IF NOT EXISTS user_config (id integer PRIMARY KEY, eco2_threshold, integer, temp_threshold real); """

    with canvas(device) as draw:
        draw.text((0, 0), 'DWindow is klaar voor gebruik!', fill='white')
        draw.text((0, 15), 'U kunt de grenswaarden instellen in het dashboard.', fill='white')

    time.sleep(8)

    while True:
        # TODO: collect configured values
        user_config = db.getUserConfig(conn)
        # TODO: check if we need more values
        temp_thres = 25
        eco2_thres = 410

        # Collect sensor values
        temp = 20
        eco2 = 400

        # temperature = ('temperature: {:.2f}'.format(bme680.temperature))
        # humidity = ('Humidity: {:.2f}%'.format(bme680.humidity))
        # eCO2 = ('2CO2: {:.2f}ppm' .format(sgp30.eCO2))
        # TVOC = ('TVOC: {:.2f}ppb' .format(sgp30.TVOC))

        with canvas(device) as draw:
            draw.text((0, 0), "Tempratuur: ".format(temp), fill='white')
            draw.text((0, 0), "eCO2: ".format(eco2), fill='white')

        shouldWindowOpen = False

        # Add weather api raining chance
        if (eco2 > eco2_thres):
            shouldWindowOpen = True
        elif(temp > temp_thres):
            shouldWindowOpen = True

        if (shouldWindowOpen):
            openWindow()
        else: 
            closeWindow()

        time.sleep(delay)

    # while True:
    #     with canvas(device) as draw:
    #         eCO2, TVOC = sgp30.iaq_measure()
    #         # print("eCO2 = %d ppm \t TVOC = %d ppb" % (eCO2, TVOC))

    #         eCO2 = ('2CO2: {:.2f}ppm' .format(sgp30.eCO2))
    #         TVOC = ('TVOC: {:.2f}ppb' .format(sgp30.TVOC))

    #         # draw.text((0, 0), temperature, fill='white')
    #         # draw.text((0, 15), humidity, fill='white')
    #         draw.text((0, 30), eCO2, fill='white')
    #         draw.text((0, 45), TVOC, fill='white')

    #     time.sleep(1)

        # closeWindow()
        # time.sleep(1)
        # openWindow()
        # time.sleep(1)
    
    # openWindow()
    # closeWindow()

    return
    while True:
        try:
            now = datetime.now()
            # print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
            # print("Gas: %d ohm" % bme680.gas)
            # print("Humidity: %0.1f %%" % bme680.relative_humidity)
            # print("Pressure: %0.3f hPa" % bme680.pressure)
            # print("Altitude = %0.2f meters" % bme680.altitude)

            if keyPadNumber == "1":
                dateMessage = '{:%d %B %Y}'.format(now)
                timeMessage = '{:%H :%M :%S}'.format(now)
                # setPinNeutral()
                # showMessage(timeMessage, dateMessage, 'Dwindow', 18)
            if keyPadNumber == "2":
                title = "Temperatuur"
                temperature = "%0.1f C" % (bme680.temperature + temperature_offset)
                timeMessage = '{:%H :%M :%S}'.format(now)

                if bme680.temperature + temperature_offset:
                    realTemp = bme680.temperature + temperature_offset
                    print("realtemp " + str(realTemp))
                    if realTemp < 20:
                        # setPinGreen()
                        closeWindow()
                    if realTemp >= 20 and realTemp < 22:
                        # setPinYellow()
                        print('setPinYellow')
                    if realTemp >= 22:
                        # setPinRed()
                        openWindow()
                # showMessage(title, temperature, timeMessage)
            if keyPadNumber == "3":
                title = "Luchtdruk"
                pressure = "%0.3f hPa" % bme680.pressure
                timeMessage = '{:%H :%M :%S}'.format(now)
                # showMessage(title, pressure, timeMessage)
            if keyPadNumber == "4":
                title = "Luchtvochtigheid"
                pressure = " %0.1f %%" % bme680.relative_humidity
                timeMessage = '{:%H :%M :%S}'.format(now)
                # showMessage(title, pressure, timeMessage)

            readLine(L1, ["1","2","3","A"])
            readLine(L2, ["4","5","6","B"])
            readLine(L3, ["7","8","9","C"])
            readLine(L4, ["*","0","#","D"])
    
            time.sleep(delay)
        except KeyboardInterrupt:
            print("\nApplication stopped!")
        
main()