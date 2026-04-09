import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Definitions
PWM_PIN = 18 
DIR_PIN_1 = 23 
DIR_PIN_2 = 24 

GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN_1, GPIO.OUT)
GPIO.setup(DIR_PIN_2, GPIO.OUT)

# Initialize PWM 
motor_pwm = GPIO.PWM(PWM_PIN, 1000)
GPIO.output(DIR_PIN_1, GPIO.HIGH)
GPIO.output(DIR_PIN_2, GPIO.LOW)    
motor_pwm.start(0) 

# Variables
speed = 0

def change_speed(speed):
    if speed < 100:
        speed += 1
    else:
        speed = 0
    return speed
    
try:
    print("Motor running, press Ctrl+C to stop")  
    # Infinite loop 
    while True:
        speed = change_speed(speed)
        motor_pwm.ChangeDutyCycle(speed)
        print(speed)
        time.sleep(0.5) 
        
except KeyboardInterrupt:
    print("\nShutdown...")

finally:
    motor_pwm.stop()
    GPIO.cleanup()
    print("Done.")