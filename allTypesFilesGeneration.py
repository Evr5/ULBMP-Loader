from image import Image
from pixel import Pixel
from encoding import Encoder
import os

download_folder = os.path.join(os.path.expanduser('~'), 'Downloads/ulbmpImages/')


pixel = []
for i in range(187500):
    pixel.append(Pixel(0, 0, 0))
print(len(pixel))
for i in range(187500):
    pixel.append(Pixel(255, 255, 255))
image1 = Image(750, 500, pixel)
Encoder(image1, 3, depth=1, rle=False).save_to(download_folder + "v3_depth1.ulbmp")
Encoder(image1, 1).save_to(download_folder + "v1_2colors.ulbmp")
Encoder(image1, 2).save_to(download_folder + "v2_2colors.ulbmp")


pixel1 = []
for i in range(93750):
    pixel1.append(Pixel(0, 0, 255))
for i in range(93750):
    pixel1.append(Pixel(0, 255, 0))
for i in range(93750):
    pixel1.append(Pixel(255, 0, 0))
for i in range(93750):
    pixel1.append(Pixel(0, 0, 0))
image2 = Image(750, 500, pixel1)
Encoder(image2, 3, depth=2, rle=False).save_to(download_folder + "v3_depth2.ulbmp")
Encoder(image2, 1).save_to(download_folder + "v1_4colors.ulbmp")
Encoder(image2, 2).save_to(download_folder + "v2_4colors.ulbmp")


pixel2 = []
for i in range(37500):
    pixel2.append(Pixel(0, 255, 0))
for i in range(37500):
    pixel2.append(Pixel(0, 0, 255))
for i in range(37500):
    pixel2.append(Pixel(0, 0, 0))
for i in range(37500):
    pixel2.append(Pixel(255, 255, 255))
for i in range(37500):
    pixel2.append(Pixel(255, 255, 0))
for i in range(37500):
    pixel2.append(Pixel(0, 255, 255))
for i in range(37500):
    pixel2.append(Pixel(255, 0, 255))
for i in range(37500):
    pixel2.append(Pixel(0, 125, 255))
for i in range(37500):
    pixel2.append(Pixel(200, 12, 0))
for i in range(37500):
    pixel2.append(Pixel(125, 0, 255))
for i in range(37500):
    pixel2.append(Pixel(213, 34, 167))
for i in range(37500):
    pixel2.append(Pixel(125, 255, 0))
for i in range(37500):
    pixel2.append(Pixel(0, 120, 56))
for i in range(37500):
    pixel2.append(Pixel(255, 125, 0))
for i in range(37500):
    pixel2.append(Pixel(175, 50, 40))
for i in range(37500):
    pixel2.append(Pixel(80, 30, 180))
image3 = Image(750, 800, pixel2)
Encoder(image3, 3, depth=4, rle=False).save_to(download_folder + "v3_depth4.ulbmp")
Encoder(image3, 1).save_to(download_folder + "v1_16colors.ulbmp")
Encoder(image3, 2).save_to(download_folder + "v2_16colors.ulbmp")


pixel3 = []
largeur = 1000
hauteur = 5
for j in range(256):
    pixel3.extend([Pixel(j, j, j)] * (largeur * hauteur))

print(len(pixel3))
image4 = Image(1600, 800, pixel3)
Encoder(image4, 3, depth=8, rle=False).save_to(
    download_folder + "v3_depth8_rle=False.ulbmp"
)
Encoder(image4, 3, depth=8, rle=True).save_to(
    download_folder + "v3_depth8_rle=True.ulbmp"
)
Encoder(image4, 1).save_to(download_folder + "v1_256colors.ulbmp")
Encoder(image4, 2).save_to(download_folder + "v2_256colors.ulbmp")


colors = []
for r in range(256):
    for g in range(256):
        for b in range(256):
            pixel = Pixel(r, g, b)
            colors.append(pixel)
image5 = Image(8192, 2048, colors)
Encoder(image5, 3, depth=24, rle=False).save_to(
    download_folder + "v3_depth24_rle=False.ulbmp"
)
Encoder(image5, 3, depth=24, rle=True).save_to(
    download_folder + "v3_depth24_rle=True.ulbmp"
)
Encoder(image5, 1).save_to(download_folder + "v1_fullcolors.ulbmp")
Encoder(image5, 2).save_to(download_folder + "v2_fullcolors.ulbmp")
