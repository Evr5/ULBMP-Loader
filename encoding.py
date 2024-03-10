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
        """
        Initialisation de la classe Encoder.
        """
        self.image = img
        self.version = version
        depth = kwargs.get('depth')
        rle = kwargs.get('rle')
        self.depth = depth
        self.rle = rle
        self.header = bytearray()
        self.palette = []
        self.checkError()

    def checkError(self):
        """
        Check s'il n'y a pas d'erreur dans la demande d'encodage.
        """
        if self.version not in [1, 2, 3, 4]:
            raise ValueError("La version de ULBMP n'est pas valide")
        # Raise une erreur si demande d'encodage RLE avec une profondeur de 1, 2 ou 4.
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
        self.header.extend([
            0x55, 0x4c, 0x42, 0x4d, 0x50,  # ULBMP en ASCII
            self.version,   # version de l'encodage ULBMP
            *self.image.width.to_bytes(2, 'little'),  # Largeur de l'image en little-endian
            *self.image.height.to_bytes(2, 'little')  # Hauteur de l'image en little-endian
        ])

        if self.version == 3:
            bytes_pixel = self.version3()
        else:
            # Ajout de la taille du header dans le header
            self.header.insert(6, 0x0c)
            self.header.insert(7, 0x00)
            if self.version == 1:
                bytes_pixel = self.version1()
            elif self.version == 2:
                bytes_pixel = self.version2()
            else:
                bytes_pixel = self.version4()

        with open(path, 'wb') as file:
            file.write(self.header)
            file.write(bytes_pixel)

    def version1(self):
        """
        Pour la version 1 de l'ULBMP, on ajoute 3 bytes (valeur Red, Green et Blue) pour chaque pixel à la liste
        bytes_pixel.
        """
        bytes_pixel = bytearray()
        for pixel in self.image.pixels:
            bytes_pixel.extend([pixel.red, pixel.green, pixel.blue])
        return bytes_pixel

    def version2(self):
        """
        Pour la version 2 de l'ULBMP, utilisation du RLE, on ajoute 2 bytes pour les mêmes pixels : 
        premier byte pour le nombre de pixels qu'il y a, le deuxième byte pour le pixel.
        """
        bytes_pixel = bytearray()
        current_pixel = self.image.pixels[0]
        same_pixel = 1  # initialisation du nombre de mêmes pixels
        for next_pixel in self.image.pixels[1:]:
            if next_pixel == current_pixel and same_pixel < 255:
                same_pixel += 1
            else:
                bytes_pixel.extend([same_pixel, current_pixel.red, current_pixel.green, current_pixel.blue])
                current_pixel = next_pixel
                same_pixel = 1
        # ajout des derniers pixels
        bytes_pixel.extend([same_pixel, current_pixel.red, current_pixel.green, current_pixel.blue])
        return bytes_pixel

    def version3(self):
        """
        Pour la version 3 de l'ULBMP, encodage spécifique au depth et RLE spécifié.
        """
        def palette(self):
            """
            Création de la plalette en fonction des différentes couleurs rencontrées dans l'image.
            """
            unique_colors = set()
            for pixel in self.image.pixels:
                unique_colors.add((pixel.red, pixel.green, pixel.blue))
            # Ajoute les différentes couleurs à la palette
            for color in unique_colors:
                self.palette.append(list(color))

        def updateHeader(self):
            """
            Met à jour le header en ajoutant la taille du header et la palette.
            """
            self.header.extend((self.depth, self.rle))   # ajout de la profondeur et de l'encodage RLE (ou non)
            # Ajout de la palette dans le header pour les profondeurs 1, 2, 4 et 8.
            if self.depth in [1, 2, 4, 8]:
                palette = bytes(sum(self.palette, []))
                self.header.extend(palette)
            len_header = len(self.header) + 2   # +2 pour les 2 bytes qui spécifient la taille du header
            self.header[6:6] = len_header.to_bytes(2, 'little')  # ajout de la taille du header

        def depth1_2_4(self):
            """
            Encodage pour les depth 1, 2 et 4 qui n'auront jamais de RLE.
            """
            # création du string du format attendu pour la valeur binaire de la profondeur
            depth_version = '0' + str(self.depth) + 'b'
            pixel_bits = []  # création de la liste de stockage des valeurs binaires de la profondeur
            bytes_pixel = bytearray()
            for pixel in self.image.pixels:
                pixel_index = self.palette.index([pixel.red, pixel.green, pixel.blue])
                pixel_bits.extend(format(pixel_index, depth_version))
                # Si la valeur contient 8 bits, on l'ajoute à la liste des bytes à écrire
                if len(pixel_bits) == 8:
                    bytes_pixel.append(int(''.join(pixel_bits), 2))
                    pixel_bits = []
            # S'il reste des bits
            if pixel_bits:
                remaining_bits = 8 - len(pixel_bits)    # calcul du nombre de bits à rajouter
                pixel_bits += ('0' * remaining_bits)    # complète le nombre binaire avec des 0
                bytes_pixel.append(int(''.join(pixel_bits), 2))   
            return bytes_pixel

        def depth8(self):
            """
            Encodage pour depth 8 avec ou sans RLE.
            """
            if not self.rle:
                pixel_bits = []  # création de la liste de stockage des valeurs binaires de la profondeur
                bytes_pixel = bytearray()
                for pixel in self.image.pixels:
                    pixel_bits.extend(format(self.palette.index([pixel.red, pixel.green, pixel.blue]), '08b'))
                    bytes_pixel.append(int(''.join(pixel_bits), 2))
                    pixel_bits = []
            else:
                bytes_pixel = bytearray()
                current_pixel = self.image.pixels[0]
                same_pixel_count = 1
                for next_pixel in self.image.pixels[1:]:
                    if next_pixel == current_pixel and same_pixel_count < 255:
                        same_pixel_count += 1
                    else:
                        pixel_index = self.palette.index([current_pixel.red, current_pixel.green, current_pixel.blue])
                        bytes_pixel.extend([same_pixel_count, pixel_index])
                        current_pixel = next_pixel
                        same_pixel_count = 1
                pixel_index = self.palette.index([current_pixel.red, current_pixel.green, current_pixel.blue])
                bytes_pixel.extend([same_pixel_count, pixel_index])
            return bytes_pixel

        def depth24(self):
            """
            Encodage pour depth 24 avec au sans RLE. Comme c'est le même principe que la version 1 ou 2,
            utilisation de la fonction d'encodage version2 pour RLE, sinon version1.
            """
            if self.rle:
                bytes_pixel = self.version2()   # même méthode que pour version 2
            else:
                bytes_pixel = self.version1()   # même méthode que pour version 1
            return bytes_pixel

        palette(self)   # Création de la plalette
        updateHeader(self)  # Ajout de la taille du header et de la palette
        if self.depth == 24:
            bytes_pixel = depth24(self)
        else:
            if self.depth in [1, 2, 4]:
                bytes_pixel = depth1_2_4(self)
            elif self.depth == 8:
                bytes_pixel = depth8(self)
        return bytes_pixel 

    def version4(self):
        def ULBMP_SMALL_DIFF(bytes_pixel, Dr, Dg, Db):
            nb_bin = int("00" + format(Dr + 2, '02b') + format(Dg + 2, '02b') + format(Db + 2, '02b'), 2)
            bytes_pixel.extend([nb_bin])

        def ULBMP_INTERMEDIATE_DIFF(bytes_pixel, Dr, Dg, Db):
            nb_byte0 = int("01" + format(Dg + 32, '06b'), 2)
            nb_byte1 = int(format(Dr - Dg + 8, '04b') + format(Db - Dg + 8, '04b'), 2)
            bytes_pixel.extend([nb_byte0, nb_byte1])

        def ULBMP_BIG_DIFF_R(bytes_pixel, Dr, Dg, Db):
            if Dr + 128 <= 0:
                print("Dr : ", Dr)
                print("Dr + 128 = ", Dr + 128)
            Dr_bin = format(Dr + 128, '08b')
            if int(Dr_bin, 2) <= 2:
                print("Dr_bin : ", Dr_bin)
            Dg_Dr_bin = format(Dg - Dr + 32, '06b')
            nb_bin1 = int("1000" + Dr_bin[:4], 2)
            nb_bin2 = int(Dr_bin[4:] + Dg_Dr_bin[:2], 2)
            nb_bin3 = int(Dg_Dr_bin[4:] + format(Db - Dr + 32, '06b'), 2)
            bytes_pixel.extend([nb_bin1, nb_bin2, nb_bin3])

        def ULBMP_BIG_DIFF_G(bytes_pixel, Dr, Dg, Db):
            Dg_bin = format(Dg + 128, '08b')
            Dr_Dg_bin = format(Dr - Dg + 32, '06b')
            nb_bin1 = int("1001" + Dg_bin[:4], 2)
            nb_bin2 = int(Dg_bin[4:] + Dr_Dg_bin[:2], 2)
            nb_bin3 = int(Dr_Dg_bin[4:] + format(Db - Dg + 32, '06b'), 2)
            bytes_pixel.extend([nb_bin1, nb_bin2, nb_bin3])

        def ULBMP_BIG_DIFF_B(bytes_pixel, Dr, Dg, Db):
            Db_bin = format(Db + 128, '08b')
            Dr_Db_bin = format(Dr - Db + 32, '06b')
            nb_bin1 = int("1010" + Db_bin[:4], 2)
            nb_bin2 = int(Db_bin[4:] + Dr_Db_bin[:2], 2)
            nb_bin3 = int(Dr_Db_bin[4:] + format(Dg - Db + 32, '06b'), 2)
            bytes_pixel.extend([nb_bin1, nb_bin2, nb_bin3])

        def ULBMP_NEW_PIXEL(bytes_pixel, pixel):
            bytes_pixel.extend([255, pixel.red, pixel.green, pixel.blue])


        current_pixel = Pixel(0, 0, 0)
        bytes_pixel = bytearray()
        for pixel in self.image.pixels:
            Dr = pixel.red - current_pixel.red
            Dg = pixel.green - current_pixel.green
            Db = pixel.blue - current_pixel.blue
            if -2 <= Dr <= 1 and -2 <= Dg <= 1 and -2 <= Db <= 1:
                ULBMP_SMALL_DIFF(bytes_pixel, Dr, Dg, Db)
            elif -32 <= Dg <= 31 and -8 <= (Dr - Dg) <= 7 and  -8 <= (Db - Dg) <= 7:
                ULBMP_INTERMEDIATE_DIFF(bytes_pixel, Dr, Dg, Db)
            elif -128 <= Dr <= 127 and -32 <= (Dg - Dr) <= 31 and -32 <= (Db - Dr) <= 31:
                ULBMP_BIG_DIFF_R(bytes_pixel, Dr, Dg, Db)
            elif -128 <= Dg <= 127 and -32 <= (Dr - Dg) <= 31 and -32 <= (Db - Dg) <= 31:
                ULBMP_BIG_DIFF_G(bytes_pixel, Dr, Dg, Db)
            elif -128 <= Db <= 127 and -32 <= (Dr - Db) <= 31 and -32 <= (Dg - Db) <= 31:
                ULBMP_BIG_DIFF_B(bytes_pixel, Dr, Dg, Db)
            else:
                ULBMP_NEW_PIXEL(bytes_pixel, pixel)
            current_pixel = pixel
        
        return bytes_pixel


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
        """
        Vérifie s'il n'y a pas d'erreur dans le header.
        """
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
        for i in range(0, len(pixels_bytes), 3):
            pixels.append(Pixel(pixels_bytes[i], pixels_bytes[i + 1], pixels_bytes[i + 2]))

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
                Decoder.version1(pixels_bytes, pixels)  # même méthode que pour version 1
            else:
                Decoder.version2(pixels_bytes, pixels)  # même méthode que pour version 2

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
        def ULBMP_NEW_PIXEL(pixels_bytes, pixels, i):
            pixels.append(Pixel(pixels_bytes[i + 1], pixels_bytes[i + 2], pixels_bytes[i + 3]))
            i += 4
            current_pixel = pixels[-1]
            return i, current_pixel

        def ULBMP_SMALL_DIFF(pixels, i, current_pixel_bytes, current_pixel):
            Dr = int(current_pixel_bytes[2:4], 2) - 2
            dgreen = int(current_pixel_bytes[4:6], 2) - 2
            dblue = int(current_pixel_bytes[6:], 2) - 2
            red = Dr + current_pixel.red
            green = dgreen + current_pixel.green
            blue = dblue + current_pixel.blue
            pixels.append(Pixel(red, green, blue))
            i += 1
            current_pixel = pixels[-1]
            return i, current_pixel

        def ULBMP_INTERMEDIATE_DIFF(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
            second_bytes = format(pixels_bytes[i + 1], '08b')
            dgreen = int(current_pixel_bytes[2:], 2) - 32
            Dr_Dg = int(second_bytes[:4], 2) - 8
            Db_Dg = int(second_bytes[4:], 2) - 8
            green = dgreen + current_pixel.green
            red = Dr_Dg + current_pixel.red + green - current_pixel.green
            blue = Db_Dg + current_pixel.blue + green - current_pixel.green
            pixels.append(Pixel(red, green, blue))
            i += 2
            current_pixel = pixels[-1]
            return i, current_pixel


        def ULBMP_BIG_DIFF_R(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
            second_bytes = format(pixels_bytes[i + 1], '08b')
            last_byte = format(pixels_bytes[i + 2], '08b')
            Dr = int(current_pixel_bytes[4:] + second_bytes[:4], 2) - 128
            Dg_Dr = int(second_bytes[4:] + last_byte[:2], 2) - 32
            Db_Dr = int(last_byte[2:], 2) - 32
            red = Dr + current_pixel.red
            green = Dg_Dr + current_pixel.green + red - current_pixel.red
            blue = Db_Dr + current_pixel.blue + red - current_pixel.red
            pixels.append(Pixel(red, green, blue))
            i += 3
            current_pixel = pixels[-1]
            return i, current_pixel

        def ULBMP_BIG_DIFF_G(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
            second_bytes = format(pixels_bytes[i + 1], '08b')
            last_byte = format(pixels_bytes[i + 2], '08b')
            Dg = int(current_pixel_bytes[4:] + second_bytes[:4], 2) - 128
            Dr_Dg = int(second_bytes[4:] + last_byte[:2], 2) - 32
            Db_Dg = int(last_byte[2:], 2) - 32
            green = Dg + current_pixel.green
            red = Dr_Dg + current_pixel.red + green - current_pixel.green
            blue = Db_Dg + current_pixel.blue + green - current_pixel.green
            pixels.append(Pixel(red, green, blue))
            i += 3
            current_pixel = pixels[-1]
            return i, current_pixel

        def ULBMP_BIG_DIFF_B(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel):
            second_bytes = format(pixels_bytes[i + 1], '08b')
            last_byte = format(pixels_bytes[i + 2], '08b')
            Db = int(current_pixel_bytes[4:] + second_bytes[:4], 2) - 128
            Dr_Db = int(second_bytes[4:] + last_byte[:2], 2) - 32
            Dg_Db = int(last_byte[2:], 2) - 32
            blue = Db + current_pixel.blue
            red = Dr_Db + current_pixel.red + blue - current_pixel.blue
            green = Dg_Db + current_pixel.green + blue - current_pixel.blue
            pixels.append(Pixel(red, green, blue))
            i += 3
            current_pixel = pixels[-1]
            return i, current_pixel

        current_pixel = Pixel(0, 0, 0)
        i = 0
        while len(pixels) != number_pixel:
            current_pixel_bytes = format(pixels_bytes[i], '08b')
            if current_pixel_bytes == '11111111':
                i, current_pixel = ULBMP_NEW_PIXEL(pixels_bytes, pixels, i)
            elif current_pixel_bytes[:2] == '00':
                i, current_pixel = ULBMP_SMALL_DIFF(pixels, i, current_pixel_bytes, current_pixel)
            elif current_pixel_bytes[0:2] == '01':
                i, current_pixel = ULBMP_INTERMEDIATE_DIFF(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
            elif current_pixel_bytes[0:4] == '1000':
                i, current_pixel = ULBMP_BIG_DIFF_R(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
            elif current_pixel_bytes[0:4] == '1001':
                i, current_pixel = ULBMP_BIG_DIFF_G(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
            elif current_pixel_bytes[0:4] == '1010':
                i, current_pixel = ULBMP_BIG_DIFF_B(pixels_bytes, pixels, i, current_pixel_bytes, current_pixel)
                
        return pixels
    