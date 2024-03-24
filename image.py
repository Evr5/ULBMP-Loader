"""
NOM : Van Ruyskensvelde
PRÉNOM : Ethan
SECTION : B1-INF0
MATRICULE : 000589640
"""
from pixel import Pixel


class Image:
    def __init__(self, width, height, pixels):
        """
        Initialisation de la classe Image
        """
        if width*height != len(pixels):
            raise ValueError("La longueur et largeur sont différent du nombre de pixels")

        if not isinstance(pixels, list):
            raise ValueError("Pixel doit être une liste de pixels")

        for pixel in pixels:
            if not isinstance(pixel, Pixel):
                raise ValueError("Le contenu de la liste pixels doit être des objets Pixel")
            
        self.width = width
        self.height = height
        self.pixels = pixels

    def __str__(self):
        """
        Affiche la classe avec la largeur, hauteur et le contenu de la liste pixel
        """
        show = ""
        for y in range(self.height):
            for x in range(self.width):
                show += str(self[x, y]) + " "
            show += "\n"
        return show

    def __getitem__(self, pos):
        """
        Surcharge l’opérateur [] en lecture
        """
        x, y = pos
        #  si pos n’est pas une position valide dans l’image
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            raise IndexError("Position hors limite")
        return self.pixels[y * self.width + x]

    def __setitem__(self, pos, pix):
        """
        Surcharge l’opérateur [] en écriture
        """
        x, y = pos
        # si pos n’est pas une position valide dans l’image
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            raise IndexError("Position hors limite")
        self.pixels[y * self.width + x] = pix

    def __eq__(self, other):
        """
        Surcharge l’opérateur d'égalité

        """
        if not isinstance(other, Image):
            res = False
        else:
            res = (self.width, self.height, self.pixels) == (other.width, other.height, other.pixels)
        return res
