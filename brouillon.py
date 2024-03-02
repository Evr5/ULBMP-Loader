# Convertir la chaîne de bytes en un entier
byte_string = b'\xff'
integer_value = int.from_bytes(byte_string, byteorder='big')

# Convertir cet entier en sa représentation binaire
binary_representation = bin(integer_value)

# Afficher la représentation binaire
print(binary_representation)


if binary_representation == bin(255):
    print("yes")