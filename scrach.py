# Définir les valeurs de Db, Dg et Dr
nombre_binaire = "00" + format(1, '06b')
print(type(nombre_binaire))
# Concaténer les bits dans l'ordre spécifi
print(nombre_binaire)
print(nombre_binaire[4:])

# Convertir le nombre binaire en un octet
octet = int(nombre_binaire, 2).to_bytes(1, byteorder='big')

print(octet)



