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
from pixel import Pixel


pixel = []

for i in range (400*200):
    pixel.append(Pixel(0, 0, 0))
    pixel.append(Pixel(255, 0, 0))
    pixel.append(Pixel(0, 0, 255))
    pixel.append(Pixel(0, 255, 0))
    
print(len(pixel))
