import os

# --- Helper to create a dummy file for testing (optional, remove for production) ---
def create_dummy_file(filename):
    """Creates a small dummy file for testing the functions."""
    try:
        with open(filename, "w") as f:
            f.write("This is the first line.\n")
            f.write("Second line here.\n")
            f.write("And the third.\n")
            f.write("Finally, the last line.\n")
    except OSError as e:
        print(f"Error creating dummy file {filename}: {e}")

# --- Core MicroPython function for counting lines and getting size ---
def file_len_efficient(fname):
    """
    Counts lines and gets file size efficiently for MicroPython.
    Returns (line_count, file_size_bytes) or (None, None) on error.
    """
    line_count = 0
    try:
        with open(fname, 'r') as f: # Explicitly open in read mode
            for line_count, l in enumerate(f):
                pass # Just iterate to count lines
        
        # In MicroPython, os.stat() returns a tuple, where index 6 is the file size (st_size)
        statinfo = os.stat(fname)
        
        # enumerate is 0-indexed, so add 1 for the total count of lines
        return line_count + 1, statinfo[6] 
    except OSError as e:
        # Catch OSError if the file doesn't exist or there's another file system error
        print(f"Error accessing file {fname}: {e}")
        return None, None # Return None to indicate an error

# --- Example Usage ---
test_filename = "myFile.txt"
create_dummy_file(test_filename) # Create a file for the example to run

lines, size = file_len_efficient(test_filename)
if lines is not None and size is not None:
    print(f"Number of lines in '{test_filename}': {lines}")
    print(f"Size of '{test_filename}': {size} bytes")
else:
    print(f"Failed to get info for '{test_filename}'.")

# Clean up the dummy file (optional)
try:
    os.remove(test_filename)
except OSError:
    pass # Ignore if file was not created or already removed
