import os
import machine
import time

# Initialize SD card
# slot=2 typically refers to VSPI (SPI2) on ESP32
# Ensure your wiring matches the default SPI pins or specify them explicitly
# For default VSPI: sck=18, miso=19, mosi=23, cs=5
try:
    sd = machine.SDCard(slot=2) # Or slot=1 for HSPI, or define custom pins
    os.mount(sd, "/sd")
    print("SD card mounted successfully to /sd")
except Exception as e:
    print(f"Error mounting SD card: {e}")
    print("Please check wiring and ensure SD card is formatted (FAT/FAT32).")
    # A short delay before potentially restarting or exiting for debugging
    time.sleep(5)
    machine.reset() # Reset if SD card fails to mount

# List directory contents
try:
    contents = os.listdir('/sd')
    print("Directory contents on /sd:", contents)
except OSError as e:
    print(f"Error listing directory contents: {e}")

# Unmount the SD card (optional, but good practice when done)
try:
    os.umount("/sd")
    print("SD card unmounted successfully.")
except Exception as e:
    print(f"Error unmounting SD card: {e}")
