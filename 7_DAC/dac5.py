from machine import DAC, Pin, reset
import time
import math

dac = DAC(Pin(25))

notes = [
    523,   # C (Octave 5)
    587,   # D
    659,   # E
    698,   # F
    784,   # G
    880,   # A
    988,   # B
    1046   # C (Octave 6)
]

samples = 25
wave = []
for i in range(samples):
    angle = 2 * math.pi * i / samples
    wave.append(int((math.sin(angle) + 1) * 127.5))  # 0–255

def play_tone(freq, duration_ms=300):
    delay_us = int(1000000 / (freq * samples))
    end_time = time.ticks_ms() + duration_ms
    while time.ticks_ms() < end_time:
        for val in wave:
            dac.write(val)
            time.sleep_us(delay_us)

for i in range(8):
    play_tone(notes[i])
for i in range(8):
    play_tone(notes[i], duration_ms=1000)

reset()