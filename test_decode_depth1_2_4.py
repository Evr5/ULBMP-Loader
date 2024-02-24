"""
    def depth1(pixels_bytes, pixels, number_pixel, colors):
        bits = ''
        for i in pixels_bytes:
            bits += format(int(i), '08b')
        index = 0
        while len(pixels) < number_pixel and index < len(bits):
            bit = bits[index]
            pixels.append(Pixel(colors[int(bit)][0], colors[int(bit)][1], colors[int(bit)][2]))
            index += 1
        return pixels

    def depth2(pixels_bytes, pixels, number_pixel, colors):
        bits = ''
        for i in pixels_bytes:
            bits += format(int(i), '08b')
        index = 0
        while index < len(bits) - 1 and len(pixels) < number_pixel:
            valeur = int(bits[index:index + 2], 2)
            pixels.append(Pixel(colors[valeur][0], colors[valeur][1], colors[valeur][2]))
            index += 2
        return pixels

    def depth4(pixels_bytes, pixels, number_pixel, colors):
        bits = ''
        for i in pixels_bytes:
            bits += format(int(i), '08b')
        index = 0
        while index < len(bits) - 3 and len(pixels) < number_pixel:
            valeur = int(bits[index:index + 4], 2)
            pixels.append(Pixel(colors[valeur][0], colors[valeur][1], colors[valeur][2]))
            index += 4
        return pixels
"""
from pixel import Pixel


def depth_2_4(depth_version, pixels_bytes, pixels, number_pixel, colors):
    bits = ''
    for i in pixels_bytes:
            bits += format(int(i), '08b')
    index = 0
    while len(pixels) < number_pixel and index < len(bits) - (depth_version - 1):
            valeur = int(bits[index:index + depth_version], 2)
            pixels.append(Pixel(colors[valeur][0], colors[valeur][1], colors[valeur][2]))
            index += depth_version
    return pixels