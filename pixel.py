"""
NOM : Van Ruyskensvelde
PRÉNOM : Ethan
SECTION : B1-INF0
MATRICULE : 000589640
"""


class Pixel:
    def __init__(self, red, green, blue):
        if not (0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255):
            raise ValueError("Les valeurs RGB ne sont pas comprises entre 0 et 255")
        self.__red = red
        self.__green = green
        self.__blue = blue

    @property
    def red(self):
        return self.__red

    @property
    def green(self):
        return self.__green

    @property
    def blue(self):
        return self.__blue

    def __repr__(self):
        return f"Pixel({self.red}, {self.green}, {self.blue})"

    def __eq__(self, other):
        if isinstance(other, Pixel):
            res = (self.red, self.green, self.blue) == (other.red, other.green, other.blue)
        else:
            res = False
        return res
