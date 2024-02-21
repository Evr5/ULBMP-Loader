"""# Liste des pixels avec des couleurs différentes
pixels = []

# Générer 256 couleurs différentes
for red in range(0, 256, 64):  # 0, 64, 128, 192
    for green in range(0, 256, 64):  # 0, 64, 128, 192
        for blue in range(0, 256, 64):  # 0, 64, 128, 192
            # Ajouter 40 pixels de la même couleur
            for _ in range(100):
                pixels.append(Pixel(red, green, blue))

print(len(pixels), ": au début")

image = Image(80, 80, pixels)

encoder = Encoder(image, 3, depth=8, rle=True)

encoder.save_to("C:/Users/ethan/Downloads/rle_true.ulbmp")
"""

header = bytearray([0x55, 0x4c, 0x42, 0x4d, 0x50])
test = bytes([int(True)])
header += test
print(header)

