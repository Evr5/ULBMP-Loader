"""
NOM : Van Ruyskensvelde
PRÉNOM : Ethan
SECTION : B1-INF0
MATRICULE : 000589640
"""
from pixel import Pixel
from image import Image
import time


class Encoder:
    def __init__(self, img, version=1, **kwargs):
        """
        Initialisation de la classe Encoder.
        """
        self.image = img
        self.version = version
        depth = kwargs.get('depth')
        rle = kwargs.get('rle')
        self.depth = depth
        self.rle = rle
        self.checkError()

    def checkError(self):
        if self.version not in [1, 2, 3, 4]:
            raise ValueError("La version de ULBMP n'est pas valide")
        if self.rle and self.depth in [1, 2, 4]:
            raise ValueError("L'encodage RLE n'est disponible que pour une profondeur de 8 ou 24")
        
        if self.version == 3:
            if not self.depth:
                raise ValueError("Il manque le choix de profondeur")
            elif self.rle not in [True, False]:
                raise ValueError("Le choix de l'encodage rle n'est pas spécifié")
            
    def save_to(self, path):
        """
        Encodage d'un fichier ULBMP au path spécifié.
        """
        header = bytearray([
            0x55, 0x4c, 0x42, 0x4d, 0x50,  # ULBMP en ASCII
            self.version,
            *self.image.width.to_bytes(2, 'little'),  # Largeur de l'image en little-endian
            *self.image.height.to_bytes(2, 'little')  # Hauteur de l'image en little-endian
        ])
        if self.version == 3:
            self.version3(path, header)
        else:
            # Ajout de la taille du header dans le header
            header.insert(6, 0x0c)
            header.insert(7, 0x00)
            with open(path, 'wb') as file:
                file.write(header)
                if self.version == 1:
                    self.version1(file)
                elif self.version == 2:
                    self.version2(file)
                else:
                    self.version4(file)

    def version1(self, file):
        """
        Pour la version 1 de l'ULBMP, on écrit 3 bytes pour chaque pixel.
        """
        for pixel in self.image.pixels:
            file.write(bytes([pixel.red, pixel.green, pixel.blue]))

    def version2(self, file):
        """
        Pour la version 2 de l'ULBMP, utilisation du RLE, on écrit 2 bytes pour les mêmes pixels : 
        premier bytes pour le nombre de pixels qu'il y a, le deuxième bytes pour le pixel.
        """
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
        """
        Pour la version 3 de l'ULBMP, encodage spécifique au depth et RLE spécifié.
        """
        header = self.updateHeader(header)  # Ajout de la taille du header et de la palette
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

    def version4(self, file):
        pass

    def palette(self):
        """
        Création de la plalette en fonction des différentes couleurs rencontrées dans l'image.
        """
        unique_colors = set()
        for pixel in self.image.pixels:
            unique_colors.add((pixel.red, pixel.green, pixel.blue))
        return [list(color) for color in unique_colors]
    
    def updateHeader(self, header):
        """
        Ajout de la taille du header et de la palette dans le header.
        """
        header.extend((self.depth, self.rle))
        if self.depth in [1, 2, 4, 8]:
            palette = bytes(sum(self.palette(), []))
            header.extend(palette)
        len_header = len(header) + 2
        header[6:6] = len_header.to_bytes(2, 'little')
        return header
    
    def depth1_2_4(self, palette):
        """
        Encodage pour les depth 1, 2 et 4 qui n'auront jamais de RLE.
        """
        bin_format = "0"
        bin_format += str(self.depth) + "b"
        
        pixel_bits = []
        pixel_bytes = bytearray()
        for pixel in self.image.pixels:
            pixel_index = palette.index([pixel.red, pixel.green, pixel.blue])
            pixel_bits.extend(format(pixel_index, bin_format))
            if len(pixel_bits) >= 8:
                byte_to_write = pixel_bits[:8]
                pixel_bits = pixel_bits[8:]
                pixel_bytes.append(int(''.join(byte_to_write), 2))
                
        # Si des bits restent à écrire à la fin
        if pixel_bits:
            remaining_bits_count = 8 - len(pixel_bits)
            pixel_bits.extend('0' * remaining_bits_count)
            pixel_bytes.append(int(''.join(pixel_bits), 2))
        return pixel_bytes
    
    def depth8(self, palette):
        """
        Encodage pour depth 8 avec ou sans RLE.
        """
        if not self.rle:
            pixel_bits = []
            pixel_bytes = bytearray()
            for pixel in self.image.pixels:
                pixel_bits.extend(format(palette.index([pixel.red, pixel.green, pixel.blue]), '08b'))
                pixel_bytes.append(int(''.join(pixel_bits), 2))
                pixel_bits.clear()
        else:
            pixel_bytes = bytearray()
            current_pixel = self.image.pixels[0]
            same_pixel_count = 1
            for next_pixel in self.image.pixels[1:]:
                if next_pixel == current_pixel and same_pixel_count < 255:
                    same_pixel_count += 1
                else:
                    pixel_index = palette.index([current_pixel.red, current_pixel.green, current_pixel.blue])
                    pixel_bytes.extend([same_pixel_count, pixel_index])
                    current_pixel = next_pixel
                    same_pixel_count = 1
            pixel_index = palette.index([current_pixel.red, current_pixel.green, current_pixel.blue])
            pixel_bytes.extend([same_pixel_count, pixel_index])
        return pixel_bytes
    
    def depth24(self, file):
        """
        Encodage pour depth 24 avec au sans RLE. Comme c'est le même principe que la version 1 ou 2,
        utilisation de la fonction d'encodage version2 pour RLE, sinon version1.
        """
        if self.rle:
            self.version2(file)
        else:
            self.version1(file)
    

class Decoder:
    def load_from(path):
        """
        Charge l'image depuis son emplacement pour créer un objet Image qui contient des objets de type Pixel.
        """     
        content = Decoder.fileContent(path)
        version = int(content[5])
        header_size = int.from_bytes(content[6:8], 'little')
        header = content[: header_size]

        Decoder.checkErrors(header, version)

        width = int.from_bytes(header[8:10], 'little')
        height = int.from_bytes(header[10:12], 'little')
        number_pixel = height * width
        pixels_bytes = content[header_size:]
        pixels = Decoder.decode_pixels(version, header, pixels_bytes, number_pixel)
        return Image(width, height, pixels)
    
    def checkErrors(header, version):
        if version not in [1, 2, 3, 4]:
            raise ValueError("La version de ULBMP n'est pas valide")
        
        elif header[:5] != bytes([0x55, 0x4c, 0x42, 0x4d, 0x50]):
            raise ValueError("Il y a eu un problème lors de la lecture de l'image:\n'Mauvais format: il manque"
                             " 'ULBMP' dans l'en-tête")
    
    def fileContent(path):
        """
        Ouvre et lit le contenu du fichier.
        """
        with open(path, 'rb') as file:
            return file.read()

    def decode_pixels(version, header, pixels_bytes, number_pixel):
        """
        En fonction de la version, renvoie vers la fonction appropriée.
        """
        pixels = []
        if version == 1:
            Decoder.version1(pixels_bytes, pixels)
        elif version == 2:
            Decoder.version2(pixels_bytes, pixels)
        elif version == 3:
            Decoder.version3(header, pixels_bytes, pixels, number_pixel)
        else:
            Decoder.version4(pixels_bytes, pixels, number_pixel)
        return pixels

    def version1(pixels_bytes, pixels):
        """
        Ajoute à la liste pixels chaques objets Pixel en prenant byte par byte le rouge, le vert et le bleu du pixel.
        """
        start = time.time()
        for i in range(0, len(pixels_bytes), 3):
            pixels.append(Pixel(pixels_bytes[i], pixels_bytes[i + 1], pixels_bytes[i + 2]))
        end = time.time()
        print("temps de chargenent v1 : ", end-start, " secondes")

    def version2(pixels_bytes, pixels):
        """
        Ajoute à la liste pixels chaques objets Pixel en prenant byte par byte le rouge, le vert et le bleu du pixel, 
        en le faisant avec le principe du RLE, donc le premier byte est le nombre de fois qu'il faut ajouter le même
        pixel.
        """
        i = 0
        while i < len(pixels_bytes):
            for _ in range(pixels_bytes[i]):
                pixels.append(Pixel(pixels_bytes[i + 1], pixels_bytes[i + 2], pixels_bytes[i + 3]))
            i += 4

    def version3(header, pixels_bytes, pixels, number_pixel):
        """
        Ajoute à la liste pixels chaques objets Pixel avec le principe de la pelette de couleurs.
        """
        def paletteCreation(palette):
            """
            Récupère la palette et la stocke dans une liste.
            """
            colors = []
            for i in range(0, len(palette), 3):
                colors.append([int(palette[i]), int(palette[i + 1]), int(palette[i + 2])])
            return colors

        def depth_1_to_4(pixels_bytes, pixels, number_pixel, depth_number, colors):
            """
            Ajoute à la liste pixels chaques objets Pixel pour un encodage de depth 1, 2 et 4 qui n'aura jamais de RLE.
            """
            bits_list = []
            for i in pixels_bytes:
                bits_list.extend(format(int(i), '08b'))
            index = 0
            while len(pixels) < number_pixel and index < len(bits_list) - (depth_number - 1):
                valeur = int(''.join(bits_list[index:index + depth_number]), 2)
                pixels.append(Pixel(colors[valeur][0], colors[valeur][1], colors[valeur][2]))
                index += depth_number

        def depth8(pixels_bytes, pixels, rle, colors):
            """        
            Ajoute à la liste pixels chaques objets Pixel pour un encodage de depth 8 avec ou sans RLE.
            """
            if not rle:
                for i in pixels_bytes:
                    pixels.append(Pixel(colors[i][0], colors[i][1], colors[i][2]))
            else:
                i = 0
                while i < len(pixels_bytes):
                    count = pixels_bytes[i]
                    value_byte = int(pixels_bytes[i + 1])
                    for _ in range(count):
                        pixels.append(Pixel(colors[value_byte][0], colors[value_byte][1], colors[value_byte][2]))
                    i += 2

        def depth24(pixels_bytes, pixels, rle):
            """
            Décodage pour depth 24 avec au sans RLE. Comme c'est le même principe que la version 1 ou 2,
            utilisation de la fonction d'encodage version2 pour RLE, sinon version1.
            """
            if not rle:
                Decoder.version1(pixels_bytes, pixels)
            else:
                Decoder.version2(pixels_bytes, pixels)


        depth_number, rle, palette = header[12], bool(header[13]), header[14:]
        colors = paletteCreation(palette)

        if depth_number in [1, 2, 4]:
            pixels = depth_1_to_4(pixels_bytes, pixels, number_pixel, depth_number, colors)
        elif depth_number == 8:
            pixels = depth8(pixels_bytes, pixels, rle, colors)
        elif depth_number == 24:
            depth24(pixels_bytes, pixels, rle)
            
        return pixels
    
    def version4(pixels_bytes, pixels, number_pixel):
        current_pixel = Pixel(0, 0, 0)
        i = 0
        while len(pixels) != number_pixel:
            current_pixel_bytes = pixels_bytes[i]
            if current_pixel_bytes == b'\xff':
                i, current_pixel = Decoder.ULBMP_NEW_PIXEL(pixels_bytes, pixels, i)
            elif bin(int.from_bytes(current_pixel_bytes, 'big'))[2:4] == '00':
                i, current_pixel = Decoder.ULBMP_SMALL_DIFF(pixels, i, current_pixel_bytes, current_pixel)
            elif bin(int.from_bytes(current_pixel_bytes, 'big'))[2:4] == '01':
                i, current_pixel = Decoder.ULBMP_INTERMEDIATE_DIFF(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
            elif bin(int.from_bytes(current_pixel_bytes, 'big'))[2:6] == '1000':
                i, current_pixel = Decoder.ULBMP_BIG_DIFF_R(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
            elif bin(int.from_bytes(current_pixel_bytes, 'big'))[2:6] == '1001':
                i, current_pixel = Decoder.ULBMP_BIG_DIFF_G(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
            elif bin(int.from_bytes(current_pixel_bytes, 'big'))[2:6] == '1010':
                i, current_pixel = Decoder.ULBMP_BIG_DIFF_B(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
        return pixels

    def ULBMP_NEW_PIXEL(pixels_bytes, pixels, i):
        pixels.append(Pixel(pixels_bytes[i + 1], pixels_bytes[i + 2], pixels_bytes[i + 3]))
        i += 4
        current_pixel = pixels[-1]
        return i, current_pixel

    def ULBMP_SMALL_DIFF(pixels, i, current_pixel_bytes, current_pixel):
        Dr = int.from_bytes(current_pixel_bytes, 'big')[4:6]
        dgreen = int.from_bytes(current_pixel_bytes, 'big')[6:8]
        dblue = int.from_bytes(current_pixel_bytes, 'big')[-2:]
        red = Dr + current_pixel.red
        green = dgreen + current_pixel.green
        blue = dblue + current_pixel.blue
        pixels.append(Pixel(red, green, blue))
        i += 1
        current_pixel = pixels[-1]
        return i, current_pixel

    def ULBMP_INTERMEDIATE_DIFF(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
        second_bytes = pixels_bytes[i + 1]
        dgreen = int.from_bytes(current_pixel_bytes, 'big')[-6:]
        Dr_Dg = int.from_bytes(second_bytes, 'big')[2:6]
        Db_Dg = int.from_bytes(second_bytes, 'big')[-4:]
        green = dgreen + current_pixel.green
        red = Dr_Dg + current_pixel.red + green - current_pixel.green 
        blue = Db_Dg + current_pixel.blue + green - current_pixel.green
        pixels.append(Pixel(red, green, blue))
        i += 2
        current_pixel = pixels[-1]
        return i, current_pixel


    def ULBMP_BIG_DIFF_R(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
        second_bytes = pixels_bytes[i + 1]
        last_byte = pixels_bytes[i + 2]
        Dr = int((int.from_bytes(current_pixel_bytes, 'big'))[-4:] + bin(int.from_bytes(second_bytes, 'big'))[2:6], 2)
        Dg_Dr = int((int.from_bytes(second_bytes, 'big'))[-4:] + bin(int.from_bytes(last_byte, 'big'))[2:4], 2)
        Db_Dr = int.from_bytes(last_byte, 'big')[-6:]
        red = Dr + current_pixel.red
        green = Dg_Dr + current_pixel.green + red - current_pixel.red
        blue = Db_Dr + current_pixel.blue + red - current_pixel.red
        pixels.append(Pixel(red, green, blue))
        i += 3
        current_pixel = pixels[-1]
        return i, current_pixel

    def ULBMP_BIG_DIFF_G(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
        second_bytes = pixels_bytes[i + 1]
        last_byte = pixels_bytes[i + 2]
        Dg = int((int.from_bytes(current_pixel_bytes, 'big'))[-4:] + bin(int.from_bytes(second_bytes, 'big'))[2:6], 2)
        Dr_Dg = int((int.from_bytes(second_bytes, 'big'))[-4:] + bin(int.from_bytes(last_byte, 'big'))[2:4], 2)
        Db_Dg = int.from_bytes(last_byte, 'big')[-6:]
        green = Dg + current_pixel.green
        red = Dr_Dg + current_pixel.red + green - current_pixel.green 
        blue = Db_Dg + current_pixel.blue + green - current_pixel.green
        pixels.append(Pixel(red, green, blue))
        i += 3
        current_pixel = pixels[-1]
        return i, current_pixel

    def ULBMP_BIG_DIFF_B(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
        second_bytes = pixels_bytes[i + 1]
        last_byte = pixels_bytes[i + 2]
        Db = int((int.from_bytes(current_pixel_bytes, 'big'))[-4:] + bin(int.from_bytes(second_bytes, 'big'))[2:6], 2)
        Dr_Db = int((int.from_bytes(second_bytes, 'big'))[-4:] + bin(int.from_bytes(last_byte, 'big'))[2:4], 2)
        Dg_Db = int.from_bytes(last_byte, 'big')[-6:]
        blue = Db + current_pixel.blue
        red = Dr_Db + current_pixel.red + blue - current_pixel.blue
        green = Dg_Db + current_pixel.gren + blue - current_pixel.blue
        pixels.append(Pixel(red, green, blue))
        i += 3
        current_pixel = pixels[-1]
        return i, current_pixel
