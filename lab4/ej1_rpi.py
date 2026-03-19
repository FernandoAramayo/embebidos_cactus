from gpiozero import Buzzer, Button
from signal import pause

#buzzer = Buzzer(17)
#button = Button(27, pull_up=True)

#button.when_pressed = buzzer.on
#button.when_released = buzzer.off

#pause()

buzzer = Buzzer(17)
button_on = Button(27, pull_up=True)
button_off = Button(22, pull_up=True)

def turn_on():
    buzzer.on()

def turn_off():
    buzzer.off()

button_on.when_pressed = turn_on
button_off.when_pressed = turn_off

pause()
