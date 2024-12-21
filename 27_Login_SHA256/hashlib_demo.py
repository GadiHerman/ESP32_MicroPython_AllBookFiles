# importing hashlib for getting sha256() hash function
import hashlib

def _bytes_to_hex(bytes_data):
    # A list containing all hexadecimal values
    hex_values = []  
    # Go through each byte in the data
    for byte in bytes_data:
        # Converts each byte to a hexadecimal string with a fixed length of 2 characters
        hex_value = '{:02x}'.format(byte)
        # Adds the value to the list
        hex_values.append(hex_value)   
    # concatenates all hexadecimal values ​​into a single string
    s=''
    result = s.join(hex_values) 
    return result

def _hex_to_bytes(hex_str):
    return bytes.fromhex(hex_str)

# A string that has been stored as a byte stream (due to the prefix b)
string = "1234"
# Initializing the sha256() method and passing the byte stream as an argument
sha256 = hashlib.sha256(string)
# Hashes the data, and returns the output in hexadecimal format
string_hash = sha256.digest()
print("Hash:",string_hash)
string_hash1 = _bytes_to_hex(string_hash)
print("Hash:",string_hash1)
string_hash2 = _hex_to_bytes(string_hash1)
print("Hash:",string_hash2)


newstring = "1234"
newsha256 = hashlib.sha256(string)
newstring_hash = newsha256.digest()

print(newstring_hash == string_hash)
