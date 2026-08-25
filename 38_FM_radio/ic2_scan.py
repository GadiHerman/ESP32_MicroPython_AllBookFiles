
from machine import Pin, I2C
import time

# Pin configuration
SDA_PIN = 21
SCL_PIN = 22
RESET_PIN = 25
SEN_PIN = 26

# Si4703 I2C address
SI4703_ADDRESS = 0x10


# Configure control pins
reset_pin = Pin(RESET_PIN, Pin.OUT, value=0)
sen_pin = Pin(SEN_PIN, Pin.OUT, value=1)

# Configure SDA as output temporarily.
# This is required during the Si4703 bus-mode selection sequence.
sda_pin = Pin(SDA_PIN, Pin.OUT, value=0)

# Keep the chip in reset
reset_pin.value(0)

# SEN must be high for I2C mode
sen_pin.value(1)

time.sleep_ms(10)

# Release reset
reset_pin.value(1)

time.sleep_ms(10)

# Now initialize the I2C peripheral
i2c = I2C(
    0,
    scl=Pin(SCL_PIN),
    sda=Pin(SDA_PIN),
    freq=100_000
)

print("Scanning I2C bus...")

devices = i2c.scan()

print("I2C devices:", devices)

if SI4703_ADDRESS in devices:
    print("Si4703 detected.")
else:
    print("Si4703 was not detected.")
