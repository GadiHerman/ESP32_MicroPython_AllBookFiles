import os
from machine import I2S, Pin, SPI, SDCard
import time

# Pin definitions for I2S communication
SCK_PIN = 32
WS_PIN = 25
SD_PIN = 33
I2S_ID = 0

# Audio parameters (these should match your WAV file's properties)
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.STEREO # Adjust based on your WAV file (I2S.STEREO for stereo)
SAMPLE_RATE_IN_HZ = 22_050 # Adjust based on your WAV file's sample rate
BUFFER_LENGTH_IN_BYTES = 4096 # Buffer size for reading WAV file chunks
WAV_FILE_NAME_SD = "/sd/stereol_16bit_stereo_22050Hz.wav" # Ensure this file is on your SD card

def play_wav_from_sd_card(file_name):
    """
    Plays a WAV file from an SD card via I2S.
    
    Args:
        file_name (str): The full path to the WAV file on the SD card.
    """
    print(f"Attempting to play WAV file from SD card: {file_name}")

    # Initialize SD card
    # slot=2 typically refers to VSPI (SPI2) on ESP32
    # Ensure your wiring matches the default SPI pins or specify them explicitly
    # For default VSPI: sck=18, miso=19, mosi=23, cs=5
    try:
        sd = SDCard(slot=2) # Or slot=1 for HSPI, or define custom pins
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

    # Initialize I2S peripheral
    audio_out = I2S(
        I2S_ID,
        sck=Pin(SCK_PIN),
        ws=Pin(WS_PIN),
        sd=Pin(SD_PIN),
        mode=I2S.TX,
        bits=SAMPLE_SIZE_IN_BITS,
        format=FORMAT,
        rate=SAMPLE_RATE_IN_HZ,
        ibuf=BUFFER_LENGTH_IN_BYTES,
    )

    # Open the WAV file from the SD card
    with open(file_name, "rb") as wav_file:
        # Skip WAV header (typically 44 bytes)
        wav_file.seek(44) 
        
        print("Playing audio from SD card...")
        while True:
            # Read a chunk of audio data
            audio_chunk = wav_file.read(BUFFER_LENGTH_IN_BYTES)
            if not audio_chunk:
                # End of file reached
                print("End of WAV file on SD card.")
                break
            # Write the audio chunk to I2S
            num_written = audio_out.write(audio_chunk)

    try:
        os.umount("/sd")
        print("SD card unmounted successfully.")
    except Exception as e:
        print(f"Error unmounting SD card: {e}")

# Call the function to play the WAV file from SD card
play_wav_from_sd_card(WAV_FILE_NAME_SD)
print("Done with SD card WAV playback example.")

