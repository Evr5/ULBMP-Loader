import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Affichage d'une image")

        # Créer une image à partir d'une suite de pixels (remplacez les valeurs par les vôtres)
        image_width = 200
        image_height = 200
        image_data = bytearray(image_width * image_height * 4)  # 4 bytes par pixel pour RGBA
        for y in range(image_height):
            for x in range(image_width):
                index = (y * image_width + x) * 4
                image_data[index:index+4] = bytes([255, 0, 0, 255])  # Rouge vif (RGBA)

        # Créer une QImage à partir de la suite de pixels
        qimage = QImage(image_data, image_width, image_height, QImage.Format_RGBA8888)

        # Créer un QLabel pour afficher l'image
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap.fromImage(qimage))

        # Créer un layout vertical et ajouter le QLabel
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        # Créer un widget central et assigner le layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
