# Initial setup
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import Mock.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pin setup
button1_pin = 36
button2_pin = 40
led1_pin = 12
led2_pin = 16
led3_pin = 18
led4_pin = 22

GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)
GPIO.setup(led3_pin, GPIO.OUT)
GPIO.setup(led4_pin, GPIO.OUT)

# Variables
state = -1
time_on = 1
last_change_time = 0
leds = [led1_pin, led2_pin, led3_pin, led4_pin]
selected_led = 0

def check_buttons(current_time):
    global selected_led
    global last_change_time
    global state
    global time_on
    if not GPIO.input(button1_pin):
        if state < 3:
            state += 1
        else:
            state = 0
        selected_led = leds[state]
        time_on = 1
        last_change_time = current_time
        time.sleep(0.2)
        while not GPIO.input(button1_pin):
            pass
    elif not GPIO.input(button2_pin):
        time_on += 1
        last_change_time = current_time
        time.sleep(0.2)
        while not GPIO.input(button2_pin):
            pass   

def turn_leds(selected_led, last_change_time):
    for led in leds:
        if led != selected_led:
            GPIO.output(led, GPIO.LOW)

    if selected_led in leds:
        if current_time - last_change_time >= time_on:
            GPIO.output(selected_led, GPIO.LOW)
        else:
            GPIO.output(selected_led, GPIO.HIGH)   

try:
     while True:
        current_time = time.time()           
        check_buttons(current_time)
        turn_leds(selected_led, last_change_time)
        time.sleep(0.05)

except KeyboardInterrupt:
        GPIO.cleanup() 