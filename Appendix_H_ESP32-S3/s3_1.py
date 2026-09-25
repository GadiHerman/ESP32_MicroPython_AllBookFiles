import gc

gc.collect()

free_ram = gc.mem_free()
allocated_ram = gc.mem_alloc()
total_ram = free_ram + allocated_ram

print(f"Total available Heap RAM: {total_ram / (1024 * 1024):.2f} MB")
print(f"Free Heap RAM:            {free_ram / (1024 * 1024):.2f} MB")
print(f"Allocated Heap RAM:       {allocated_ram / (1024 * 1024):.2f} MB")

buffer_size = 2 * 1024 * 1024  # 2 MegaBytes

try:
    print("\nAllocating 2MB buffer in PSRAM...")
    big_buffer = bytearray(buffer_size)
    
    big_buffer[0] = 0xAA
    big_buffer[-1] = 0xBB
    
    print(f"Buffer created successfully!")
    print(f"First byte: {hex(big_buffer[0])}, Last byte: {hex(big_buffer[-1])}")
    
    print(f"Remaining Free RAM: {gc.mem_free() / (1024 * 1024):.2f} MB")

    del big_buffer
    gc.collect()
    print("\nBuffer freed.")
    print(f"Free RAM after garbage collection: {gc.mem_free() / (1024 * 1024):.2f} MB")

except MemoryError:
    print("Failed to allocate memory! Ensure you flashed a MicroPython build with SPIRAM support.")
