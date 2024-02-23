"""
NOM : Van Ruyskensvelde
PRÉNOM : Ethan
SECTION : B1-INF0
MATRICULE : 000589640
"""


import sys
from PySide6.QtWidgets import QApplication
from window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

print("test")


"""
test pour voir si je peux uploader ?!
"""

print("test de upload")