import math
import struct
from machine import I2S, Pin
import sys

# I2S Pin definitions for ESP32
SCK_PIN = 32
WS_PIN = 25
SD_PIN = 33

# Audio configuration parameters
I2S_ID = 0
BUFFER_BYTES = 2000
TONE_FREQ = 1000 # Frequency of the generated tone in Hz
SAMPLE_BITS = 32
AUDIO_FORMAT = I2S.MONO # Audio channel format (MONO or STEREO)
SAMPLE_RATE = 22050 # Sample rate in Hz

def Generates_sine(rate, frequency):
    """
    Generates a sine wave tone as a bytearray of samples.
    
    Args:
        rate (int): Sample rate in Hz.
        frequency (int): Frequency of the sine wave in Hz.
        
    Returns:
        bytearray: A bytearray containing the sine wave samples.
    """
    global SAMPLE_BITS 
    samples_per_cycle = rate // frequency
    sample_bytes = SAMPLE_BITS // 8
    samples = bytearray(samples_per_cycle * sample_bytes)
    
    # Reduce volume to prevent clipping
    volume_factor = 32 
    amplitude_range = (2**SAMPLE_BITS // 2) // volume_factor
      
    for i in range(samples_per_cycle):
        # Generate sine wave sample with a DC offset (as per original logic)
        sample_val = amplitude_range + int((amplitude_range - 1) * math.sin(2 * math.pi * i / samples_per_cycle))
        struct.pack_into('<l', samples, i * sample_bytes, sample_val)
    return samples

# Initialize the I2S peripheral for audio output
audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN), ws=Pin(WS_PIN), sd=Pin(SD_PIN), # I2S pins
    mode=I2S.TX, bits=SAMPLE_BITS, format=AUDIO_FORMAT, # Mode, bit depth, format
    rate=SAMPLE_RATE, ibuf=BUFFER_BYTES # Sample rate, internal buffer size
)

# Generate the sine wave samples for the tone
tone_samples = Generates_sine(SAMPLE_RATE, TONE_FREQ)
print("START playing tone")
while True:
    try:
        audio_out.write(tone_samples)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        audio_out.deinit()
        sys.exit()