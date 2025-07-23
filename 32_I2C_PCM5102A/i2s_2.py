import os
from machine import I2S, Pin

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

# Name of the WAV file stored on the ESP32
WAV_FILE_NAME = "stereol_16bit_stereo_22050Hz.wav" # Ensure this file is uploaded to your ESP32

def play_wav_from_internal_storage(file_name):
    """
    Plays a WAV file from the ESP32's internal storage via I2S.
    
    Args:
        file_name (str): The name of the WAV file to play.
    """
    print(f"Attempting to play WAV file: {file_name}")

    try:
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

        # Open the WAV file in binary read mode
        with open(file_name, "rb") as wav_file:
            # Skip WAV header (typically 44 bytes for standard WAV files)
            # For simplicity, we assume a standard WAV header.
            # In a real application, you would parse the header to get sample rate, bits, channels.
            wav_file.seek(44) 
            
            print("Playing audio...")
            while True:
                # Read a chunk of audio data from the file
                audio_chunk = wav_file.read(BUFFER_LENGTH_IN_BYTES)
                
                if not audio_chunk:
                    # End of file reached
                    print("End of WAV file.")
                    break
                
                # Write the audio chunk to the I2S peripheral
                num_written = audio_out.write(audio_chunk)
                # print(f"Written {num_written} bytes to I2S") # Optional: uncomment for debugging

    except OSError as e:
        print(f"Error opening or reading WAV file: {e}")
    except Exception as e:
        print(f"An error occurred: {type(e).__name__} - {e}")
    finally:
        # Always deinitialize I2S to release resources
        if 'audio_out' in locals() and audio_out:
            audio_out.deinit()
            print("I2S deinitialized.")

# Call the function to play the WAV file
play_wav_from_internal_storage(WAV_FILE_NAME)
print("Done with WAV playback example. ")