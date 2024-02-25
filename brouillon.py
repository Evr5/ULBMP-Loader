"""
def depth1(self, palette):
        pixel_bits = ''
        pixel_bytes = bytearray()  # Utilisation de bytearray pour modifier les octets
        for pixel in self.image.pixels:
            pixel_index = palette.index([pixel.red, pixel.green, pixel.blue])
            pixel_bits += str(format(pixel_index, '01b'))
            if len(pixel_bits) >= 8:
                while len(pixel_bits) >= 8:  # Boucler jusqu'à ce que tous les 8 bits soient pleins
                    byte_to_write = pixel_bits[:8]  # Prend les 8 premiers bits
                    pixel_bits = pixel_bits[8:]  # Supprime les 8 premiers bits de pixel_bits
                    pixel_bytes.append(int(byte_to_write, 2))  # Ajoute le byte à pixel_bytes
                if len(pixel_bits) > 0:
                    pixel_bits = pixel_bits.rjust(8, '0')  # Remplir avec des zéros à gauche si nécessaire

        # Si des bits restent à écrire à la fin
        if pixel_bits:
            remaining_bits = pixel_bits.ljust(8, '0')  # Remplir avec des zéros à droite
            pixel_bytes.append(int(remaining_bits, 2))

        return pixel_bytes

    def depth2(self, palette):
        pixel_bits = ''
        pixel_bytes = bytearray()  # Utilisation de bytearray pour modifier les octets
        for pixel in self.image.pixels:
            pixel_index = palette.index([pixel.red, pixel.green, pixel.blue])
            pixel_bits += str(format(pixel_index, '02b'))  # Deux bits par pixel
            while len(pixel_bits) >= 8:  # Boucler jusqu'à ce que tous les 8 bits soient pleins
                byte_to_write = pixel_bits[:8]  # Prend les 8 premiers bits
                pixel_bits = pixel_bits[8:]  # Supprime les 8 premiers bits de pixel_bits
                pixel_bytes.append(int(byte_to_write, 2))  # Ajoute le byte à pixel_bytes

        # Si des bits restent à écrire à la fin
        if pixel_bits:
            remaining_bits = pixel_bits.ljust(8, '0')  # Remplir avec des zéros à droite
            pixel_bytes.append(int(remaining_bits, 2))

        return pixel_bytes

    def depth4(self, palette):
        pixel_bits = ''
        pixel_bytes = bytearray()  # Utilisation de bytearray pour modifier les octets
        for pixel in self.image.pixels:
            pixel_index = palette.index([pixel.red, pixel.green, pixel.blue])
            pixel_bits += str(format(pixel_index, '04b'))  # Quatre bits par pixel
            while len(pixel_bits) >= 8:  # Boucler jusqu'à ce que tous les 8 bits soient pleins
                byte_to_write = pixel_bits[:8]  # Prend les 8 premiers bits
                pixel_bits = pixel_bits[8:]  # Supprime les 8 premiers bits de pixel_bits
                pixel_bytes.append(int(byte_to_write, 2))  # Ajoute le byte à pixel_bytes

        # Si des bits restent à écrire à la fin
        if pixel_bits:
            remaining_bits = pixel_bits.ljust(8, '0')  # Remplir avec des zéros à droite
            pixel_bytes.append(int(remaining_bits, 2))

        return pixel_bytes
"""

def depth1_2_4(self, palette):
    pixel_bits = ''
    pixel_bytes = bytearray()
    for pixel in self.image.pixels:
        pixel_index = palette.index([pixel.red, pixel.green, pixel.blue])