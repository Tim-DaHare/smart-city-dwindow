from gpiozero import Buzzer
from time import sleep

buzzerGPIO = 21

buzzer = Buzzer(buzzerGPIO)


def triggerBuzzer():
    buzzer.on()
    sleep(1)
    buzzer.off()

triggerBuzzer()