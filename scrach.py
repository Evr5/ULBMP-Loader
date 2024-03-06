current_pixel_bytes = '00001111'
second_bytes = '11110000'


a = int(current_pixel_bytes[4:] + second_bytes[:4], 2) - 128

print(a)