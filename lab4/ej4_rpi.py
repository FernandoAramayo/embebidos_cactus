from gpiozero import LED
from time import sleep
import os

led1 = LED(5)
led2 = LED(6)
led3 = LED(13)

config_file = "/home/cactus/lab4/interval.txt"

state = 0
interval = 1.0
last_mtime = 0

def read_interval():
    global last_mtime
    try:
        mtime = os.path.getmtime(config_file)
        if mtime != last_mtime:
            last_mtime = mtime
            with open(config_file, "r") as f:
                value = float(f.read().strip())
                if value > 0:
                    return value
    except:
        pass
    return None

def set_state(s):
    led1.off()
    led2.off()
    led3.off()

    if s == 0:
        led1.on()
    elif s == 1:
        led2.on()
    elif s == 2:
        led3.on()

while True:
    new_interval = read_interval()
    if new_interval is not None:
        interval = new_interval
        print(f"Nuevo intervalo: {interval} s")

    set_state(state)
    sleep(interval)
    state = (state + 1) % 3