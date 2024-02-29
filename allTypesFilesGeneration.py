from image import Image
from pixel import Pixel
from encoding import Encoder
import os

user_folder = os.path.expanduser('~')
download_folder = os.path.join(user_folder, 'Downloads') + '/allTypesULBMP/'



pixel = []
for i in range(750*50):
    pixel.append(Pixel(0, 0, 0))
for i in range(750*50):
    pixel.append(Pixel(255, 255, 255))
image1 = Image(750, 100, pixel)
Encoder(image1, 3, depth = 1, rle = False).save_to(download_folder+"v3_depth1.ulbmp")
Encoder(image1, 1).save_to(download_folder+'v1_2colors.ulbmp')
Encoder(image1, 2).save_to(download_folder+'v2_2colors.ulbmp')


for i in range(750*50):
    pixel.append(Pixel(0, 255, 0))
for i in range(750*50):
    pixel.append(Pixel(0, 0, 255))
image2 = Image(750, 200, pixel)
Encoder(image2, 3, depth = 2, rle = False).save_to(download_folder+"v3_depth2.ulbmp")
Encoder(image2, 1).save_to(download_folder+'v1_4colors.ulbmp')
Encoder(image2, 2).save_to(download_folder+'v2_4colors.ulbmp')


for i in range(750*50):
    pixel.append(Pixel(255, 255, 0))
for i in range(750*50):
    pixel.append(Pixel(0, 255, 255))
for i in range(750*50):
    pixel.append(Pixel(255, 0, 255))
for i in range(750*50):
    pixel.append(Pixel(0, 125, 255))
for i in range(750*50):
    pixel.append(Pixel(200, 12, 0))
for i in range(750*50):
    pixel.append(Pixel(125, 0, 255))
for i in range(750*50):
    pixel.append(Pixel(213, 34, 167))
for i in range(750*50):
    pixel.append(Pixel(125, 255, 0))
for i in range(750*50):
    pixel.append(Pixel(0, 120, 56))
for i in range(750*50):
    pixel.append(Pixel(255, 125, 0))
for i in range(750*50):
    pixel.append(Pixel(175, 50, 40))
for i in range(750*50):
    pixel.append(Pixel(80, 30, 180))
image3 = Image(750, 800, pixel)
Encoder(image3, 3, depth = 4, rle = False).save_to(download_folder+'v3_depth4.ulbmp')
Encoder(image3, 1).save_to(download_folder+'v1_16colors.ulbmp')
Encoder(image3, 2).save_to(download_folder+'v2_16colors.ulbmp')


for j in range(240):
    for i in range(750*1):
        pixel.append(Pixel(j, j, j))
image4 = Image(750, 1040, pixel)
Encoder(image4, 3, depth = 8, rle = False).save_to(download_folder+'v3_depth8_rle=False.ulbmp')
Encoder(image4, 3, depth = 8, rle = True).save_to(download_folder+'v3_depth8_rle=True.ulbmp')
Encoder(image4, 1).save_to(download_folder+'v1_256colors.ulbmp')
Encoder(image4, 2).save_to(download_folder+'v2_256colors.ulbmp')


pixel_24 = []
for i in range(256):
    for j in range(256):
        for k in range(256):
            pixel_24.append(Pixel(i, j, k))

print(len(pixel_24))

