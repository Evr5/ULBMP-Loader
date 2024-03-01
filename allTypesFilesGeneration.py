from image import Image
from pixel import Pixel
from encoding import Encoder
import os

user_folder = os.path.expanduser("~")
download_folder = os.path.join(user_folder, "Téléchargements/") + "allTypesULBMP/"


pixel = []
for i in range(150000):
    pixel.append(Pixel(0, 0, 0))
print(len(pixel))
for i in range(150000):
    pixel.append(Pixel(255, 255, 255))
image1 = Image(750, 400, pixel)
Encoder(image1, 3, depth=1, rle=False).save_to(download_folder + "v3_depth1.ulbmp")
Encoder(image1, 1).save_to(download_folder + "v1_2colors.ulbmp")
Encoder(image1, 2).save_to(download_folder + "v2_2colors.ulbmp")


pixel1 = []
for i in range(15000):
    pixel1.append(Pixel(0, 0, 0))
for i in range(15000):
    pixel1.append(Pixel(255, 255, 255))
for i in range(15000):
    pixel1.append(Pixel(0, 0, 0))
for i in range(15000):
    pixel1.append(Pixel(255, 255, 255))
image2 = Image(750, 80, pixel1)
Encoder(image2, 3, depth=2, rle=False).save_to(download_folder + "v3_depth2.ulbmp")
Encoder(image2, 1).save_to(download_folder + "v1_4colors.ulbmp")
Encoder(image2, 2).save_to(download_folder + "v2_4colors.ulbmp")


pixel2 = []
for i in range(30000):
    pixel2.append(Pixel(0, 255, 0))
for i in range(30000):
    pixel2.append(Pixel(0, 0, 255))
for i in range(30000):
    pixel2.append(Pixel(0, 0, 0))
for i in range(30000):
    pixel2.append(Pixel(255, 255, 255))
for i in range(30000):
    pixel2.append(Pixel(255, 255, 0))
for i in range(30000):
    pixel2.append(Pixel(0, 255, 255))
for i in range(30000):
    pixel2.append(Pixel(255, 0, 255))
for i in range(30000):
    pixel2.append(Pixel(0, 125, 255))
for i in range(30000):
    pixel2.append(Pixel(200, 12, 0))
for i in range(30000):
    pixel2.append(Pixel(125, 0, 255))
for i in range(30000):
    pixel2.append(Pixel(213, 34, 167))
for i in range(30000):
    pixel2.append(Pixel(125, 255, 0))
for i in range(30000):
    pixel2.append(Pixel(0, 120, 56))
for i in range(30000):
    pixel2.append(Pixel(255, 125, 0))
for i in range(30000):
    pixel2.append(Pixel(175, 50, 40))
for i in range(30000):
    pixel2.append(Pixel(80, 30, 180))
image3 = Image(750, 640, pixel2)
Encoder(image3, 3, depth=4, rle=False).save_to(download_folder + "v3_depth4.ulbmp")
Encoder(image3, 1).save_to(download_folder + "v1_16colors.ulbmp")
Encoder(image3, 2).save_to(download_folder + "v2_16colors.ulbmp")

pixel3 = []
for j in range(256):
    for i in range(1500):
        pixel3.append(Pixel(j, j, j))
print(len(pixel3))
image4 = Image(750, 512, pixel3)
Encoder(image4, 3, depth=8, rle=False).save_to(
    download_folder + "v3_depth8_rle=False.ulbmp"
)
Encoder(image4, 3, depth=8, rle=True).save_to(
    download_folder + "v3_depth8_rle=True.ulbmp"
)
Encoder(image4, 1).save_to(download_folder + "v1_256colors.ulbmp")
Encoder(image4, 2).save_to(download_folder + "v2_256colors.ulbmp")


pixel_24 = []
for i in range(0, 256, 6):
    for j in range(0, 256, 4):
        for k in range(0, 256, 1):
            pixel_24.append(Pixel(i, j, k))
image5 = Image(1376, 512, pixel_24)
Encoder(image5, 3, depth=24, rle=False).save_to(
    download_folder + "v3_depth24_rle=False.ulbmp"
)
Encoder(image5, 3, depth=24, rle=True).save_to(
    download_folder + "v3_depth24_rle=True.ulbmp"
)
Encoder(image5, 1).save_to(download_folder + "v1_fullcolors.ulbmp")
Encoder(image5, 2).save_to(download_folder + "v2_fullcolors.ulbmp")
