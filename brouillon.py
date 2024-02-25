"""
pixel = []

for i in range (400*200):
    pixel.append(Pixel(0, 0, 0))
    pixel.append(Pixel(255, 0, 0))
    pixel.append(Pixel(0, 0, 255))
    pixel.append(Pixel(0, 255, 0))

image = Image(800, 400, pixel)

Encoder(image, 3, depth=2, rle=False).save_to("C:/Users/ethan/Downloads/depth2.ulbmp")
"""
from pixel import Pixel


pixel = []

for i in range (400*200):
    pixel.append(Pixel(0, 0, 0))
    pixel.append(Pixel(255, 0, 0))
    pixel.append(Pixel(0, 0, 255))
    pixel.append(Pixel(0, 255, 0))
    
print(len(pixel))
