import binascii

# Example byte array
byte_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xe2\x02(ICC_PROFILE\x00\x01\x01\x00\x00\x02\x18\x00\x00\x00\x00\x02\x10\x00\x'

# Convert bytes to hex
hex_string = binascii.hexlify(byte_data).decode('ascii')

print(hex_string)
