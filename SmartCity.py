# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bme680
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
#import blinka_pkg_check
import busio
# import adafruit_ssd1306
i2c = busio.I2C(board.SCL, board.SDA)
# Create sensor object, communicating over the board's default I2C bus
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
# ccs811 = adafruit_ccs811.CCS811(i2c)

factory = PiGPIOFactory()
# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25
rgbPins = {'pinRed': 26, 'pinGreen': 19, 'pinBlue': 13}
# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

devices = i2c.scan()

oled_addr = 0x3c

display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr = oled_addr, reset = None)

display.poweron()

#clearing the display
display.fill(0)

width = display.width
height = display.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

L1 = 18
L2 = 23
L3 = 24
L4 = 25

C1 = 12
C2 = 16
C3 = 20
C4 = 21


# GPIO.setmode(GPIO.BOARD)
# for i in rgbPins:
#     GPIO.setup(rgbPins[i], GPIO.OUT)
#     GPIO.setup(rgbPins[i], GPIO.HIGH)

# pinRed = GPIO.PWIM(rgbPins['pinRed'], 2000)
# pinGreen = GPIO.PWIM(rgbPins['pinGreen'], 2000)
# pinBlue = GPIO.PWIM(rgbPins['pinBlue'], 2000)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

red = 13
green = 19
blue = 26

#LED RGB
GPIO.setup(red, GPIO.OUT) #RED
GPIO.setup(green, GPIO.OUT) #GREEN
GPIO.setup(blue, GPIO.OUT) #BLUE

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
servo = Servo(5, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000,pin_factory=factory)

GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.LOW)
GPIO.output(blue, GPIO.LOW)

keyPadNumber = "1"
workingKeypadNumbers = ["1", "2", "3", "4"]

def openWindow():
    servo.value = 0
def closeWindow():
    servo.value = 1

def setPinYellow():
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(blue, GPIO.HIGH)
def setPinRed():
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.HIGH)
def setPinGreen():
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(blue, GPIO.HIGH)
def setPinBlue():
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(green, GPIO.HIGH)
    GPIO.output(blue, GPIO.LOW)
def setPinNeutral():
    GPIO.output(red, GPIO.LOW)
    GPIO.output(green, GPIO.LOW)
    GPIO.output(blue, GPIO.LOW)

#show messages
def display_message(title, subtitle, timeMessage, bigFont, smallFont):
    draw.rectangle((0, 0, width, height), outline = 0, fill = 0)
    draw.text((0, 0), title, font = bigFont , fill = 150)
    draw.text((0, 20), subtitle, font = smallFont , fill = 150)
    draw.text((0, 40), timeMessage, font = smallFont , fill = 150)
    display.image(image)
    display.show()

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
    
def showMessage(headMessage, subMessage, timeMessage = '', bigFontSize = 16, smallFontSize = 12):
    bigFont = ImageFont.truetype("FreeSans.ttf", bigFontSize)
    smallFont = ImageFont.truetype("FreeSans.ttf", smallFontSize)

    display_message(headMessage, subMessage, timeMessage, bigFont, smallFont)

def showLED(color):
    if color == 'green':
        print()
    
def main(delay = 0.5):
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
                setPinNeutral()
                showMessage(timeMessage, dateMessage, 'Dwindow', 18)
            if keyPadNumber == "2":
                title = "Temperatuur"
                temperature = "%0.1f C" % (bme680.temperature + temperature_offset)
                timeMessage = '{:%H :%M :%S}'.format(now)

                if bme680.temperature + temperature_offset:
                    realTemp = bme680.temperature + temperature_offset
                    if realTemp < 20:
                        setPinGreen()
                        closeWindow()
                    if realTemp >= 20 and realTemp < 22:
                        setPinYellow()
                    if realTemp >= 22:
                        setPinRed()
                        openWindow()
                showMessage(title, temperature, timeMessage)
            if keyPadNumber == "3":
                title = "Luchtdruk"
                pressure = "%0.3f hPa" % bme680.pressure
                timeMessage = '{:%H :%M :%S}'.format(now)
                showMessage(title, pressure, timeMessage)
            if keyPadNumber == "4":
                title = "Luchtvochtigheid"
                pressure = " %0.1f %%" % bme680.relative_humidity
                timeMessage = '{:%H :%M :%S}'.format(now)
                showMessage(title, pressure, timeMessage)

            readLine(L1, ["1","2","3","A"])
            readLine(L2, ["4","5","6","B"])
            readLine(L3, ["7","8","9","C"])
            readLine(L4, ["*","0","#","D"])

    
            time.sleep(delay)
        except KeyboardInterrupt:
            print("\nApplication stopped!")
        
main()
