from machine import Pin
import time

led_pin = Pin(2,Pin.OUT)

while True:
    led_pin.on()
    time.sleep(1)
    led_pin.off()
    time.sleep(1)