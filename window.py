"""
NOM : Van Ruyskensvelde
PRÉNOM : Ethan
SECTION : B1-INF0
MATRICULE : 000589640
"""
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QFileDialog, QErrorMessage, QInputDialog, QMessageBox, \
    QVBoxLayout, QWidget, QHBoxLayout
from PySide6.QtGui import QPixmap, QImage, QColor, QIcon
from encoding import Encoder, Decoder
import time


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialisation de la classe MainWindow.
        """
        super().__init__()
        
        self.setWindowTitle("ULBMP Loader")
        self.setWindowIcon(QIcon("file.png"))

        self.image_label = QLabel(self)
        self.load_button = QPushButton("Charger une image", self)
        self.save_button = QPushButton("Enregistrer l'image", self)
        self.save_button.setEnabled(False)
        self.color_count_label = QLabel(self)

        self.load_button.clicked.connect(self.load_image)
        self.save_button.clicked.connect(self.save_image)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addLayout(buttons_layout)
        layout.addWidget(self.image_label)
        layout.addWidget(self.color_count_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.image = None

    def load_image(self):        
        """
        Demande à l'utilisateur l'image à charger et l'affiche dans la fenêtre.
        """ 
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, 'Ouvrir une image ULBMP')   # chargement du fichier
        start = time.time()
        if filename:
            try:
                self.image = Decoder.load_from(filename)    # définition de l'image
                self.save_button.setEnabled(True)   # image chargée donc on active le bouton de sauvegarde
                pixmap = self.displayImage()
                self.image_label.setPixmap(pixmap)
                self.ajustWindowSize()
            except Exception as e:
                # récupèrer le message d'erreur s'il y a une erreur lors du chargement de l'image
                error_dialog = QErrorMessage()
                error_dialog.showMessage(str(e))
                error_dialog.exec()    
        end = time.time()
        print(f"Temps d'upload' : {end - start} secondes")
        
    def displayImage(self):
        """
        Affiche l'image dans la fenêtre.
        """
        start = time.time()
        qimage = QImage(self.image.width, self.image.height, QImage.Format_RGB888)
        colors_set = set()  # Ensemble pour stocker les couleurs uniques

        for y in range(self.image.height):
            for x in range(self.image.width):
                pixel = self.image[x, y]
                qcolor = QColor(pixel.red, pixel.green, pixel.blue)
                qimage.setPixelColor(x, y, qcolor)
                colors_set.add((qcolor.red(), qcolor.green(), qcolor.blue()))
        # Le nombre de couleurs différentes est la longueur de l'ensemble
        number_of_colors = len(colors_set)
        # Afficher le nombre de couleurs dans un QLabel
        self.color_count_label.setText(f"Nombre de couleurs : {number_of_colors}")

        end = time.time()
        print(f"Temps d'affichage : {end - start} secondes")

        return QPixmap.fromImage(qimage)
    
    def ajustWindowSize(self):
        """
        Ajuste la taille de la fenêtre en fonction de la taille de l'image.
        """
        if self.image.width > 300 and self.image.height > 100: 
            self.setFixedSize(self.image.width, self.image.height + 100)  # ajoute 100 pour afficher entièrement l'image
        elif self.image.width <= 300 and self.image.height > 100:   
            self.setFixedSize(300, self.image.height + 100)  # ajoute 100 pour afficher entièrement l'image
        elif self.image.width > 300 and self.image.height <= 100:
            self.setFixedSize(self.image.width, 100)
        else:
            # si la taille de l'image est trop petite que pour que la taille de la fenêtre soit en fonction de la taille
            # de l'image
            self.setFixedSize(300, 100)

    def save_image(self):
        """
        Demande à l'ulisateur où et dans quelle version il veut enregistrer l'image et l'enregistre.
        """
        options = ["Version 1.0", "Version 2.0", "Version 3.0", "Version 4.0"]
        version, ok = QInputDialog.getItem(self, "Sélectionner la version", "Choisir la version du format ULBMP:",
                                           options, 0, False)
        if ok:
            if version == "Version 1.0":
                format = 1
                depth = None
                rle = None
            elif version == "Version 2.0":
                format = 2
                depth = None
                rle = None
            elif version == "Version 3.0":
                format = 3
                depth_options = [1, 2, 4, 8, 24]
                depth, ok_depth = QInputDialog.getItem(self, "Sélectionner la profondeur",
                                                       "Choisir la profondeur de couleur:",
                                                       [str(d) for d in depth_options], 0, False)
                if not ok_depth:
                    return

                depth = int(depth)
                
                if depth in [8, 24]:    # demande l'encodage RLE seulement si la profondeur est 8 ou 24

                    rle, ok_rle = QInputDialog.getItem(self, "Utilisation de RLE", "Activer l'encodage RLE ?",
                                                       ["Oui", "Non"], 0, False)
                    if not ok_rle:
                        return

                    if rle == "Oui":
                        rle = 1
                    else:
                        rle = 0
                
                else:
                    rle = 0

            elif version == "Version 4.0":
                format = 4
                depth = None
                rle = None

            filename, _ = QFileDialog.getSaveFileName(self, 'Enregistrer l\'image ULBMP', filter="ULBMP Files "
                                                                                                 "(*.ulbmp)")
            start = time.time()
            if filename:
                try:
                    encoder = Encoder(self.image, format, depth=depth, rle=rle)
                    encoder.save_to(filename)
                except Exception as e:
                    error_dialog = QErrorMessage()
                    error_dialog.showMessage(str(e))
                    error_dialog.exec()
            end = time.time()
            print(f"Temps de download : {end - start} secondes")
        else:
            QMessageBox.information(self, "Annulation", "Vous avez annulé le choix de version du format ULBMP.")
