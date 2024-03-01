import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap, QImage, QColor

class Pixel:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

def main():
    # Créer une application Qt
    app = QApplication(sys.argv)

    # Dimensions de l'image
    largeur = 500
    hauteur = 300

    # Liste de pixels
    pixels = [Pixel(250, 0, 0)] * (largeur * hauteur)

    # Créer une image Qt
    qimage = QImage(largeur, hauteur, QImage.Format_RGB888)

    # Remplir l'image avec les pixels
    for y in range(hauteur):
        for x in range(largeur):
            pixel = pixels[y * largeur + x]
            qcolor = QColor(pixel.r, pixel.g, pixel.b)
            qimage.setPixelColor(x, y, qcolor)

    # Créer un QPixmap à partir de l'image
    pixmap = QPixmap.fromImage(qimage)

    # Créer un QLabel pour afficher le QPixmap
    label = QLabel()
    label.setPixmap(pixmap)
    label.show()

    # Exécuter l'application Qt
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
