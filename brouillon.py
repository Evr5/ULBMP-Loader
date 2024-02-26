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
from pixel import Pixel

pixel = []
for i in range (750*180):
    pixel.append(Pixel(0, 0, 0))
for i in range (750*180):
    pixel.append(Pixel(255, 0, 0))
for i in range (750*180):
    pixel.append(Pixel(255, 255, 0))

print(len(pixel))

