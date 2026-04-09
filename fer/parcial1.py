import RPi.GPIO as GPIO
import serial
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Boton en la Raspberry
button1_pin = 17

# Configurar boton
GPIO.setup(button1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# UART
PUERTO = "/dev/ttyACM0"
BAUDIOS = 9600
TIMEOUT = 1

# Direction
config_file = "/home/cactus/cochi/modificar_pwm.txt"
with open(config_file, "w") as f:
    f.write("motor1: 50\n")
    f.write("motor2: 50\n")

def procesar_comando(cmd, ser):
    pwm_values = leer_pwm()
    if pwm_values is not None and len(pwm_values) >= 2:
        if cmd == "motor1":
            print("Enviando pwm motor 1")
            ser.write(f"{pwm_values[0]}\n".encode('utf-8'))
            ser.flush()
            time.sleep(0.2)
            
        elif cmd == "motor2":
            print("Enviando pwm motor 2")
            ser.write(f"{pwm_values[1]}\n".encode('utf-8'))
            ser.flush()
            time.sleep(0.2)
            
        elif cmd == "stop":
            print("Deteniendo motores")

        elif cmd == "turn1":
            turn1()

        elif cmd == "turn2":
            turn2()

        else:
            print("Comando no reconocido:", cmd)

def leer_pwm():
    try:
        pwm_values = []
        with open(config_file, "r") as f:
            for line in f:
                _, value = line.rstrip().split(":")
                value = float(value)
                if value > 0 and value <= 100:
                    pwm_values.append(value)
                else:
                    pwm_values.append(1)
            return pwm_values
    except:
        pass
    return None

def check_button(ser):
    if not GPIO.input(button1_pin):
        print("Enviando buzzer")
        ser.write(b"b\n")
        ser.flush()
        time.sleep(0.2)

        while not GPIO.input(button1_pin):
            pass

        time.sleep(0.02)

def turn1():
    with open(config_file, "w") as f:
        f.write("motor1: 40\n")
        f.write("motor2: 40\n")

def turn2():
    with open(config_file, "w") as f:
        f.write("motor1: 50\n")
        f.write("motor2: 50\n")

def main():
    ser = serial.Serial(PUERTO, BAUDIOS, timeout=TIMEOUT)
    ser.reset_input_buffer()
    time.sleep(1)

    print("Esperando comandos de la Tiva...")

    try:
        while True:
            if ser.in_waiting > 0:
                linea = ser.readline().decode("utf-8", errors="ignore").rstrip()

                if linea:
                    print("Recibido:", linea)
                    procesar_comando(linea, ser)

            # The 0 spam was completely removed here to allow clean communication.
            # The Tiva handles the stopping automatically now via its C code!

            check_button(ser)
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nApagando...")

    finally:
        GPIO.cleanup()
        ser.close()
        print("Listo.")

main()