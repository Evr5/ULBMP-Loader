"""
NOM : Van Ruyskensvelde
PRÉNOM : Ethan
SECTION : B1-INF0
MATRICULE : 000589640
"""
from pixel import Pixel
from image import Image


class Encoder:
    def __init__(self, img, version=1, **kwargs):
        self.image = img
        self.version = version
        depth = kwargs.get('depth')
        rle = kwargs.get('rle')
        self.depth = depth
        self.rle = rle
        self.checkError()

    def checkError(self):
        if self.version not in [1, 2, 3]:
            raise ValueError("La version de ULBMP n'est valide")

        if self.rle and self.depth in [1, 2, 4]:
            raise ValueError("L'encodage RLE n'est disponible que pour une profondeur de 8 ou 24")
        
        if self.version == 3:
            if not self.depth:
                raise ValueError("Il manque le choix de profondeur")
            elif self.rle not in [True, False]:
                raise ValueError("Le choix de l'encodage rle n'est pas spécifié")

    def save_to(self, path):
        header = bytearray([
            0x55, 0x4c, 0x42, 0x4d, 0x50,  # ULBMP en ASCII
            self.version,  # Version du format
            *self.image.width.to_bytes(2, 'little'),  # Largeur de l'image en little-endian
            *self.image.height.to_bytes(2, 'little')  # Hauteur de l'image en little-endian
        ])

        if self.version == 3:
            self.version3(path, header)

        else:
            header.insert(6, 0x0c)
            header.insert(7, 0x00)
            with open(path, 'wb') as file:
                file.write(header)
                if self.version == 1:
                    self.version1(file)
                elif self.version == 2:
                    self.version2(file)

    def version1(self, file):
        for pixel in self.image.pixels:
            file.write(bytes([pixel.red, pixel.green, pixel.blue]))

    def version2(self, file):
        current_pixel = self.image.pixels[0]
        same_pixel = 1
        for next_pixel in self.image.pixels[1:]:
            if next_pixel == current_pixel and same_pixel < 255:
                same_pixel += 1
            else:
                file.write(bytes([same_pixel, current_pixel.red, current_pixel.green, current_pixel.blue]))
                current_pixel = next_pixel
                same_pixel = 1
        file.write(bytes([same_pixel, current_pixel.red, current_pixel.green, current_pixel.blue]))

    def version3(self, path, header):
        header = self.updateHeader(header)

        with open(path, 'wb') as file:
            file.write(header)
            if self.depth == 24:
                self.depth24(file)
            else:
                palette = self.palette()
                if self.depth in [1, 2, 4]:
                    pixel_bytes = self.depth1_2_4(palette)
                elif self.depth == 8:
                    pixel_bytes = self.depth8(palette)
                file.write(pixel_bytes)

    def palette(self):
        palette = []
        for pixel in self.image.pixels:
            if [pixel.red, pixel.green, pixel.blue] not in palette:
                palette.append([pixel.red, pixel.green, pixel.blue])
        return palette

    def updateHeader(self, header):
        if self.version == 3:
            header += bytes([int(self.depth), int(self.rle)])
            if self.depth in [1, 2, 4, 8]:
                palette = self.palette()
                header += bytes(sum(palette, []))
            len_header = len(header) + 2  # longueur du header + les 2 bytes de la taille du header à écrire
            header[6:6] = len_header.to_bytes(2, 'little')
        return header

    def depth1_2_4(self, palette):
        bin_format = "0"
        bin_format += str(self.depth) + "b"
        
        pixel_bits = ''
        pixel_bytes = bytearray()
        for pixel in self.image.pixels:
            pixel_index = palette.index([pixel.red, pixel.green, pixel.blue])
            pixel_bits += str(format(pixel_index, bin_format))
            while len(pixel_bits) >= 8:
                byte_to_write = pixel_bits[:8]
                pixel_bits = pixel_bits[8:]
                pixel_bytes.append(int(byte_to_write, 2))
                
        # Si des bits restent à écrire à la fin
        if pixel_bits:
            remaining_bits = pixel_bits.ljust(8, '0')  # Remplir avec des zéros à droite
            pixel_bytes.append(int(remaining_bits, 2))

        return pixel_bytes

    def depth8(self, palette):
        if not self.rle:
            pixel_bits = ''
            pixel_bytes = bytes()
            for pixel in self.image.pixels:
                pixel_bits += str(format(palette.index([pixel.red, pixel.green, pixel.blue]), '08b'))
                if len(pixel_bits) == 8:
                    pixel_bytes += bytes([int(pixel_bits, 2)])
                    pixel_bits = ''

        else:
            pixel_bytes = bytes()
            count = 1
            for i in range(1, len(self.image.pixels)):
                if self.image.pixels[i] == self.image.pixels[i - 1]:
                    count += 1
                else:
                    pixel_bytes += bytes([count]) + bytes([palette.index(
                        [self.image.pixels[i - 1].red, self.image.pixels[i - 1].green, self.image.pixels[i - 1].blue])])
                    count = 1
            pixel_bytes += bytes([count]) + bytes([palette.index(
                [self.image.pixels[-1].red, self.image.pixels[-1].green, self.image.pixels[-1].blue])])

        return pixel_bytes

    def depth24(self, file):
        if self.rle:
            self.version2(file)
        else:
            self.version1(file)


class Decoder:
    def load_from(path):
        """
        Charge l'image depuis son emplacement pour créer un objet Image qui contient des objets Pixel
        """        
        content = Decoder.fileContent(path)
        version = Decoder.getVersion(content)
        header_size = int.from_bytes(content[6:8], 'little')
        header = content[: header_size]

        if header[:5] != bytes([0x55, 0x4c, 0x42, 0x4d, 0x50]):
            raise ValueError("Il y a eu un problème lors de la lecture de l'image:\n'Mauvais format: il manque"
                             " 'ULBMP' dans l'en-tête")

        width = int.from_bytes(header[8:10], 'little')
        height = int.from_bytes(header[10:12], 'little')
        number_pixel = height*width

        pixels_bytes = content[header_size:]
        pixels = Decoder.decode_pixels(version, header, pixels_bytes, number_pixel)
        return Image(width, height, pixels)
    
    def fileContent(path):
        with open(path, 'rb') as file:
            content = file.read()
        return content
    
    def getVersion(content):
        version = int(content[5])
        return version

    def decode_pixels(version, header, pixels_bytes, number_pixel):
        pixels = []
        if version == 1:
            Decoder.version1(pixels_bytes, pixels)
        elif version == 2:
            Decoder.version2(pixels_bytes, pixels)
        elif version == 3:
            Decoder.version3(header, pixels_bytes, pixels, number_pixel)
        else:
            raise ValueError("Version ULBMP non prise en charge")
        return pixels

    def version1(pixels_bytes, pixels):
        for i in range(0, len(pixels_bytes), 3):
            pixels.append(Pixel(pixels_bytes[i], pixels_bytes[i + 1], pixels_bytes[i + 2]))

    def version2(pixels_bytes, pixels):
        i = 0
        while i < len(pixels_bytes):
            for _ in range(pixels_bytes[i]):
                pixels.append(Pixel(pixels_bytes[i + 1], pixels_bytes[i + 2], pixels_bytes[i + 3]))
            i += 4

    def version3(header, pixels_bytes, pixels, number_pixel):
        depth_number, rle, palette = header[12], bool(header[13]), header[14:]
        colors = []
        for i in range(0, len(palette), 3):
            colors.append([int(palette[i]), int(palette[i + 1]), int(palette[i + 2])])

        if depth_number in [1, 2, 4]:
            pixels = Decoder.depth_1_to_4(pixels_bytes, pixels, number_pixel, depth_number, colors)
        elif depth_number == 8:
            pixels = Decoder.depth8(pixels_bytes, pixels, rle, colors)
        elif depth_number == 24:
            Decoder.depth24(pixels_bytes, pixels, rle)
            
        return pixels

    def depth_1_to_4(pixels_bytes, pixels, number_pixel, depth_number, colors):
        bits_list = []
        for i in pixels_bytes:
            bits_list.extend(format(int(i), '08b'))
        index = 0
        while len(pixels) < number_pixel and index < len(bits_list) - (depth_number - 1):
            valeur = int(''.join(bits_list[index:index + depth_number]), 2)
            pixels.append(Pixel(colors[valeur][0], colors[valeur][1], colors[valeur][2]))
            index += depth_number

    def depth8(pixels_bytes, pixels, rle, colors):
        if not rle:
            for i in pixels_bytes:
                valeur = int(i)
                pixels.append(Pixel(colors[valeur][0], colors[valeur][1], colors[valeur][2]))
        else:
            i = 0
            while i < len(pixels_bytes):
                count = pixels_bytes[i]
                value_byte = int(pixels_bytes[i + 1])
                for _ in range(count):
                    pixels.append(Pixel(colors[value_byte][0], colors[value_byte][1], colors[value_byte][2]))
                i += 2

    def depth24(pixels_bytes, pixels, rle):
        if not rle:
            Decoder.version1(pixels_bytes, pixels)
        else:
            Decoder.version2(pixels_bytes, pixels)
