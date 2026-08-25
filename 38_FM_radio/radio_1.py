from machine import Pin, I2C
import time
from si4703 import Si4703

# Pin configuration
SDA_PIN = 21
SCL_PIN = 22
RESET_PIN = 25
SEN_PIN = 26

print("Starting Si4703 radio...")

# Prepare the pins used during reset.
reset_pin = Pin(RESET_PIN, Pin.OUT, value=0)
sen_pin = Pin(SEN_PIN, Pin.OUT, value=1)

# Prepare the SDA pin in the state required during reset.
sda_startup = Pin(SDA_PIN, Pin.OUT, value=0)
time.sleep_ms(10)

# Release reset.
reset_pin.value(1)
time.sleep_ms(10)

# Create the hardware I2C bus.
i2c = I2C(
    0,
    scl=Pin(SCL_PIN),
    sda=Pin(SDA_PIN),
    freq=100_000
)

radio = Si4703(
    i2c=i2c,
    reset_pin=reset_pin,
    sen_pin=sen_pin
)

print("Initializing radio...")
radio.initialize()
print("Radio initialized.")
radio.set_volume(5)
print("Volume set.")
radio.set_frequency(94.5)
print("Frequency set.")
frequency = radio.get_frequency()
print("Current frequency: {:.1f} MHz".format(frequency))
status = radio.get_status()
print(status)