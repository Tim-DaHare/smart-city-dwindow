import time
import board
import adafruit_bme680
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from datetime import datetime
from PIL import ImageFont
import busio
import adafruit_sgp30
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
import db as db
import random
from gpiozero import Buzzer
import OpenWeatherModule as weather


# oled setup
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
device.rotate = 0 

i2c = busio.I2C(board.SCL, board.SDA)

# BME680
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

#SGP30
i2cSGP = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2cSGP)

#Baseline values: eCO2 = 0x8f87, TVOC = 0x8f55
# sgp30.iaq_init()
# sgp30.set_iaq_baseline(0x8973, 0x8AAE)
# sgp30.set_iaq_baseline(0x8f87, 0x8f55)

# set numberpad pins
L1 = 26
L2 = 19
L3 = 5 
L4 = 6 

C1 = 13
C2 = 22
C3 = 17
C4 = 27 

# set buzzer pin
buzzer = Buzzer(25)

# set servo pin
factory = PiGPIOFactory()
servo = Servo(18, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000,pin_factory=factory)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# numberpad setup
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# rgb setup
red = 16
green = 24
blue = 12

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

GPIO.output(red, GPIO.LOW)
GPIO.output(green, GPIO.LOW)
GPIO.output(blue, GPIO.LOW)

keyPadNumber = "1"

servo.value = 1

window_is_open = False
open_close_wait_time = 3
# open_close_wait_time = 60
last_open_close_time = time.time()

def openWindow():
    global window_is_open
    global last_open_close_time

    window_is_open = True
    last_open_close_time = time.time()
    print("window open")
    servo.value = 0

def closeWindow():
    global window_is_open
    global last_open_close_time

    window_is_open = False
    last_open_close_time = time.time()
    print("window close")
    servo.value = 1

def flashingLed(colorPin):
    for _ in range(3):
        GPIO.output(colorPin, 1)
        time.sleep(0.2)
        GPIO.output(colorPin, 0)
        time.sleep(0.2)
    
def buzz():
    buzzer.on()
    time.sleep(1)
    buzzer.off()

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

def should_window_open(conn, celcius, eco2, pop):
    user_config = db.getUserConfig(conn)

    temp_thres = user_config[0]
    eco2_thres = user_config[1]

    shouldWindowOpen = False

    if (eco2 > eco2_thres):
        shouldWindowOpen = True
    if(celcius > temp_thres):
        shouldWindowOpen = True
    if(pop > 80):
        shouldWindowOpen = False

    print(shouldWindowOpen)
    return shouldWindowOpen

small_font = ImageFont.truetype('FreeSans.ttf', 12)
font_14 = ImageFont.truetype('FreeSans.ttf', 14)
medium_font = ImageFont.truetype('FreeSans.ttf', 20)
large_font = ImageFont.truetype('FreeSans.ttf', 32)

def showMessage(temperature, humidity, eCO2, TVOC):
    with canvas(device) as draw:
        draw.text((1, 0), temperature, fill='white')
        draw.text((1, 15), humidity, fill='white')
        draw.text((1, 30), eCO2, fill='white')
        draw.text((1, 45), TVOC, fill='white')
    
def main(delay = 0.5):
    conn = db.create_connection(r"sensor_dataset.db")

    # Db init
    if conn is None:
        raise Exception("connection could not be created")

    with conn:
        create_dr_q = """CREATE TABLE IF NOT EXISTS data_readings (id integer PRIMARY KEY, measured_at text, temprature real, eco2 integer, tvoc integer, precipitation_chance integer, window_open tinyint);"""
        db.create_table(conn, create_dr_q)

        create_vth_q = """CREATE TABLE IF NOT EXISTS user_config (eco2_threshold integer, temp_threshold real); """
        db.create_table(conn, create_vth_q)

        if (db.getUserConfig(conn) == None):
            conn.cursor().execute('''INSERT INTO user_config (eco2_threshold, temp_threshold) VALUES(600, 25 )''')

    # with canvas(device) as draw:
    #     draw.text((0, 0), 'DWindow is klaar voor gebruik!', fill='white')
    #     draw.text((0, 15), 'U kunt de grenswaarden instellen in het dashboard.', fill='white')

    time.sleep(8)

    while True:
        # Collect sensor values
        # eco2 = 20
        # celcius = 18
        # tvoc = 100
        
        eco2 = sgp30.eCO2
        celcius = bme680.temperature
        tvoc = sgp30.TVOC

        # with canvas(device) as draw:
        #     draw.text((0, 0), "Tempratuur in celcius:".format(celcius), fill='white')
        #     draw.text((0, 0), "eCO2: ".format(eco2), fill='white')

        if (time.time() > last_open_close_time + open_close_wait_time):
            pop = weather.get_weather_prediction()
            #pop = 35
            shouldWindowOpen = should_window_open(conn, celcius, eco2, pop)

            # Buzz and open/close window
            if (window_is_open != shouldWindowOpen):
                buzz()
                if (shouldWindowOpen):
                    flashingLed(green)
                    openWindow()
                else: 
                    flashingLed(red)
                    closeWindow()


            # if (shouldWindowOpen):
            #     openWindow()
            # else: 
            #     closeWindow()

            # TODO: Add db record
            db.insertDataReading(conn, (celcius, eco2, tvoc, pop, int(shouldWindowOpen)))
            
            
        try:
            now = datetime.now()
            if keyPadNumber == "1":
                currentTime = '{:%H:%M:%S}'.format(now)
                currentDate = '{:%d %B %Y}'.format(now)
                with canvas(device) as draw:
                    draw.text((0, 0), currentTime, font=large_font, fill='white')
                    draw.text((0, 50), currentDate, font=small_font, fill='white')
            if keyPadNumber == "2":
                temperature = ('temperatuur: {:.2f}'.format(bme680.temperature))
                humidity = ('Vochtigheid: {:.2f}%'.format(bme680.humidity))
                eCO2 = ('CO2: {:.2f}ppm' .format(sgp30.eCO2))
                TVOC = ('TVOC: {:.2f}ppb' .format(sgp30.TVOC))
                showMessage(temperature, humidity, eCO2, TVOC)
            if keyPadNumber == "3":
                title = 'Neerslagkans:'
                verwachting = ('{} %'.format(pop))
                with canvas(device) as draw:
                    draw.text((0, 0), title, font=medium_font, fill='white')
                    draw.text((40, 20), verwachting, font=large_font, fill='white')
            if keyPadNumber == "4":
                temperature = ('temperatuur: {:.2f}'.format(bme680.temperature))
                eCO2 = ('CO2: {:.2f}ppm' .format(sgp30.eCO2))
                with canvas(device) as draw:
                    draw.text((0, 0), temperature, font=font_14, fill='white')
                    draw.text((0, 15), eCO2, font=font_14, fill='white')
            readLine(L1, ["1","2","3","A"])
            readLine(L2, ["4","5","6","B"])
            readLine(L3, ["7","8","9","C"])
            readLine(L4, ["*","0","#","D"])

            time.sleep(0.4)
        except KeyboardInterrupt:
            print("\nApplication stopped!")

        time.sleep(delay)


main()