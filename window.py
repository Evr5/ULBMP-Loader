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


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialisation de la classe MainWindow.
        """
        super().__init__()
        
        self.setWindowTitle("ULBMP Loader")
        self.setWindowIcon(QIcon("icons/file.png"))

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

    def load_image(self):        
        """
        Demande à l'utilisateur l'image à charger et l'affiche dans la fenêtre.
        """ 
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, 'Ouvrir une image ULBMP')
        if filename:
            try:
                self.image = Decoder.load_from(filename)
                self.update_color_count(filename)
                self.save_button.setEnabled(True)
                pixmap = self.display_image()
                self.image_label.setPixmap(pixmap)
                # taille convenable pour que la taille de la fenêtre soit en fonction de la taille de l'image
                if self.image.width > 300 and self.image.height > 100: 
                    self.setFixedSize(self.image.width, self.image.height)
                else:   # si la taille de l'image est trop petite que pour que la taille de la fenêtre soit en fonction de la taille de l'image
                    self.setFixedSize(300, 100)
            except Exception as e:
                error_dialog = QErrorMessage()
                error_dialog.showMessage(str(e))
                error_dialog.exec()    
        

    def display_image(self):
        """
        Affiche l'image dans la fenêtre.
        """
        pixel_bytes = bytearray()
        for pixel in self.image.pixels:
            pixel_bytes.extend([pixel.red, pixel.green, pixel.blue])
        q_image = QImage(pixel_bytes, self.image.width, self.image.height, QImage.Format_RGB888)
        return QPixmap.fromImage(q_image)

    def update_color_count(self, filename):
        """
        Affiche le nombre de couleurs différentes qu'il y a dans l'image.
        """
        content = Decoder.fileContent(filename)
        if Decoder.getVersion(content) == 3:
            # Obtenez tous les pixels de l'image
            pixels = self.image.pixels

            # Utilisez une compréhension de liste pour extraire les couleurs uniques
            unique_colors = { (pixel.red, pixel.green, pixel.blue) for pixel in pixels }

            # Utilisez la longueur de l'ensemble pour obtenir le nombre de couleurs uniques
            num_unique_colors = len(unique_colors)

            # Afficher le nombre de couleurs uniques dans le label
            self.color_count_label.setText(f"Nombre de couleurs : {num_unique_colors}")
        else:
            self.color_count_label.setText("")

    def save_image(self):
        """
        Demande à l'ulisateur où et dans quelle version il veut enregistrer l'image et l'enregistre.
        """
        options = ["Version 1.0", "Version 2.0", "Version 3.0"]
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
                
                if depth in [8, 24]:

                    rle, ok_rle = QInputDialog.getItem(self, "Utilisation de RLE", "Activer l'encodage RLE ?",
                                                    ["Oui", "Non"], 0, False)
                    if not ok_rle:
                        return

                    rle = 1 if rle == "Oui" else 0
                
                else:
                    rle = 0

            filename, _ = QFileDialog.getSaveFileName(self, 'Enregistrer l\'image ULBMP',
                                                      filter="ULBMP Files (*.ulbmp)")
            if filename:
                try:
                    encoder = Encoder(self.image, format, depth=depth, rle=rle)
                    encoder.save_to(filename)
                except Exception as e:
                    error_dialog = QErrorMessage()
                    error_dialog.showMessage(str(e))
                    error_dialog.exec()
        else:
            QMessageBox.information(self, "Annulation", "Vous avez annulé le choix de version du format ULBMP.")
