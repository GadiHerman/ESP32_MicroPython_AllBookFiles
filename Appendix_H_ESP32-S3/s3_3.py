import time
import gc

try:
    from ulab import numpy as np
    has_ulab = True
except ImportError:
    has_ulab = False
    print("Warning: 'ulab' module not found. Please use a MicroPython firmware with ulab included.")

N = 1000

print(f"--- Running Benchmark on Vector Size: {N} ---\n")

# ==========================================
# 1. Pure Python Loop
# ==========================================

list_a = [i * 0.1 for i in range(N)]
list_b = [i * 0.2 for i in range(N)]

gc.collect()
start_time = time.ticks_us()

list_c = [list_a[i] + list_b[i] for i in range(N)]

end_time = time.ticks_us()
python_time = time.ticks_diff(end_time, start_time) / 1000.0 # המרה למאי-שניות

print(f"1. Pure Python Loop Time: {python_time:.2f} ms")


# ==========================================
# 2. ulab (NumPy)
# ==========================================
if has_ulab:
    arr_a = np.array(list_a, dtype=np.float)
    arr_b = np.array(list_b, dtype=np.float)

    gc.collect()
    start_time = time.ticks_us()

    arr_c = arr_a + arr_b

    end_time = time.ticks_us()
    ulab_time = time.ticks_diff(end_time, start_time) / 1000.0

    print(f"2. ulab (Vector/SIMD) Time: {ulab_time:.2f} ms")
    
    speedup = python_time / ulab_time
    print(f"\n---> Vector acceleration is {speedup:.1f}x FASTER!")
