try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO

import time
import random

GPIO.setmode(GPIO.BOARD)

heater_led = 12
fan = 16

GPIO.setup(heater_led, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)

try:
    while True:
        temperature = random.uniform(5, 30)

        print("Temperature:", round(temperature,2), "°C")

        if temperature < 12:
            GPIO.output(heater_led, 1)
            GPIO.output(fan, 0)

        elif temperature > 20:
            GPIO.output(heater_led, 0)
            GPIO.output(fan, 1)

        else:
            GPIO.output(heater_led, 0)
            GPIO.output(fan, 0)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()