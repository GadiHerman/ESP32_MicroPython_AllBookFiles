import os
import machine
import time

# --- Setup SD card ---
try:
    sd = machine.SDCard(slot=2) # Or slot=1, or define custom pins
    os.mount(sd, "/sd")
    print("SD card mounted successfully to /sd")
except Exception as e:
    print(f"Error mounting SD card: {e}")
    print("Please check wiring and ensure SD card is formatted (FAT/FAT32).")
    time.sleep(5)
    machine.reset() # Reset if SD card fails to mount

file_path = "/sd/my_data.txt"

# --- 1. Save (Create/Write) to a file ---
print("\n--- Saving data to file ---")
data_to_write = "Hello, MicroPython on SD Card!\nThis is line 2.\n"
try:
    with open(file_path, "w") as file: # "w" mode for writing (overwrites if exists)
        file.write(data_to_write)
    print(f"Data successfully written to {file_path}")
except Exception as e:
    print(f"Error writing to file: {e}")

# --- 2. Read from a file ---
print("\n--- Reading data from file ---")
try:
    with open(file_path, "r") as file: # "r" mode for reading
        read_data = file.read()
    print(f"Content of {file_path}:\n{read_data}")
except OSError as e:
    print(f"Error reading file (file might not exist): {e}")
except Exception as e:
    print(f"An unexpected error occurred while reading: {e}")

# --- 3. Update (Append) to a file ---
print("\n--- Appending data to file ---")
data_to_append = "This is a new line appended to the file.\n"
try:
    with open(file_path, "a") as file: # "a" mode for appending (adds to end)
        file.write(data_to_append)
    print(f"Data successfully appended to {file_path}")
except Exception as e:
    print(f"Error appending to file: {e}")

# Read again to show updated content
print("\n--- Reading updated file content ---")
try:
    with open(file_path, "r") as file:
        updated_data = file.read()
    print(f"Updated content of {file_path}:\n{updated_data}")
except Exception as e:
    print(f"Error reading updated file: {e}")

# --- 4. Delete a file ---
print("\n--- Deleting the file ---")
try:
    os.remove(file_path)
    print(f"File {file_path} deleted successfully.")
except OSError as e:
    print(f"Error deleting file (file might not exist): {e}")
except Exception as e:
    print(f"An unexpected error occurred while deleting: {e}")

# Verify deletion by trying to list directory (optional)
print("\n--- Directory contents after deletion ---")
try:
    contents_after_delete = os.listdir('/sd')
    print("Directory contents on /sd:", contents_after_delete)
except OSError as e:
    print(f"Error listing directory after deletion: {e}")


# --- Unmount SD card (recommended) ---
try:
    os.umount("/sd")
    print("\nSD card unmounted successfully.")
except Exception as e:
    print(f"Error unmounting SD card: {e}")
