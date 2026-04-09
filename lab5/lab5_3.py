import RPi.GPIO as GPIO
import time

# Pin Definitions
PWM_PIN = 18 
DIR_PIN_1 = 23 
DIR_PIN_2 = 24 

# Setup 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(DIR_PIN_1, GPIO.OUT)
GPIO.setup(DIR_PIN_2, GPIO.OUT)

# Initialize PWM 
motor_pwm = GPIO.PWM(PWM_PIN, 1000)

try:
    print("Motor running, press Ctrl+C to stop")
    
    GPIO.output(DIR_PIN_1, GPIO.HIGH)
    GPIO.output(DIR_PIN_2, GPIO.LOW)
    
    motor_pwm.start(75) 
    
    # Infinite loop 
    while True:
        time.sleep(1) 
        
except KeyboardInterrupt:
    print("\nShutdown...")

finally:
    motor_pwm.stop()
    GPIO.cleanup()
    print("Done.")