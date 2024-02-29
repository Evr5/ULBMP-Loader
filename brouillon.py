"""
pixel_bytes = bytearray()
count = 1
for i in range(1, len(self.image.pixels)):
    if self.image.pixels[i] == self.image.pixels[i - 1]:
        count += 1
    else:
        # Diviser count en octets individuels
        while count > 0:
            byte_value = count % 256  # Récupérer le reste de la division de count par 256
            pixel_bytes.append(byte_value)  # Ajouter l'octet à pixel_bytes
            count //= 256  # Diviser count par 256 pour obtenir le prochain octet

        # Ajout de l'index de la couleur dans la palette
        color_index = palette.index([self.image.pixels[i - 1].red, self.image.pixels[i - 1].green, self.image.pixels[i - 1].blue])
        pixel_bytes.append(color_index)

        count = 1

# Ajout des derniers octets
while count > 0:
    byte_value = count % 256
    pixel_bytes.append(byte_value)
    count //= 256

return pixel_bytes
"""
from image import Image
from pixel import Pixel
pixel_24 = []
for i in range(0, 256, 6):
    for j in range(0, 256, 4):
        for k in range(0, 256, 1):
            pixel_24.append(Pixel(i, j, k))

list = [2, 8, 89, 56, 1, 456]
if 8 in list:
    print(True)
if 0 not in list:
    print("ok")
if 456 in list:
    print(True)
if 5 in list:
    print(False)