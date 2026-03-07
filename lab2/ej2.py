try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    import Mock.GPIO as GPIO
import time


class CounterLED:

    def __init__(self):

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self.button1_pin = 36
        self.button2_pin = 40
        self.led1_pin = 12
        self.led2_pin = 16
        self.led3_pin = 18
        self.led4_pin = 22

        GPIO.setup(self.button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.button2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.led1_pin, GPIO.OUT)
        GPIO.setup(self.led2_pin, GPIO.OUT)
        GPIO.setup(self.led3_pin, GPIO.OUT)
        GPIO.setup(self.led4_pin, GPIO.OUT)

        self.state = 0
        self.last_state = -1

    def run(self):

        try:
            while True:

                if not GPIO.input(self.button1_pin):
                    if self.state < 15:
                        self.state += 1
                    else:
                        self.state = 0

                    time.sleep(0.2)

                    while not GPIO.input(self.button1_pin):
                        pass

                elif not GPIO.input(self.button2_pin):
                    if self.state > 0:
                        self.state -= 1

                    time.sleep(0.2)

                    while not GPIO.input(self.button2_pin):
                        pass

                led_states = format(self.state, '04b')

                GPIO.output(self.led1_pin, int(led_states[0]))
                GPIO.output(self.led2_pin, int(led_states[1]))
                GPIO.output(self.led3_pin, int(led_states[2]))
                GPIO.output(self.led4_pin, int(led_states[3]))

                if self.state != self.last_state:
                    print("current number:")
                    print(self.state)
                    print(led_states)
                    print(hex(self.state))

                self.last_state = self.state

                time.sleep(0.05)

        except KeyboardInterrupt:
            GPIO.cleanup()


program = CounterLED()
program.run()