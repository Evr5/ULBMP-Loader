

decimal_val = bin(int.from_bytes(b'\xff', 'big'))[2:4] + bin(int.from_bytes(b'\xff', 'big'))[2:4]
print(int(decimal_val, 2))