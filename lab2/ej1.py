# Initial setup
try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import Mock.GPIO as GPIO

import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Pin setup
button_pin = 36
led1_pin = 12
led2_pin = 18

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led1_pin, GPIO.OUT)
GPIO.setup(led2_pin, GPIO.OUT)

# Variables
state = 1
last_blink_time = 0
led_on = False
led_states = [False, False]

# Functions
def check_buttons():
    global state
    if not GPIO.input(button_pin):
        if state < 4:
            state += 1
        else:
            state = 1
        time.sleep(0.2)
        while not GPIO.input(button_pin):
            pass

def change_state(current_time):
    global state
    global last_blink_time
    global led_on
    global led_states 
    match state:
        case 1:
            if current_time - last_blink_time >= 1:
                led_on = not led_on
                led_states[0] = led_on
                led_states[1] = not led_on
                last_blink_time = current_time
        case 2:
            if current_time - last_blink_time >= 2:
                led_on = not led_on
                led_states[0] = led_on
                led_states[1] = led_on
                last_blink_time = current_time
        case 3:
            led_states[0] = True
            led_states[1] = True
        case 4:
            led_states[0] = False
            led_states[1] = False
    return led_states

try:
    while True:  
        current_time = time.time()  
        check_buttons()
        led_states = change_state(current_time)
        GPIO.output(led1_pin, led_states[0])
        GPIO.output(led2_pin, led_states[1])
        time.sleep(0.05)
except KeyboardInterrupt:
        GPIO.cleanup() 


