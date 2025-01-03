# Projet ULBMP Loader

## Description

Ce projet est une application de chargement et de sauvegarde d'images au format ULBMP. Il permet de charger des images, de les afficher, de compter le nombre de couleurs uniques et de les sauvegarder dans différentes versions du format ULBMP.

## Installation

1. Clonez le dépôt :

    ```bash
    git clone https://github.com/Evr5/ULBMP-Loader.git
    cd projet2
    ```

2. Installez les dépendances requises :

    ```bash
    pip install PySide6
    ```

## Utilisation

1. Lancez l'application :

    ```bash
    python main.py
    ```

2. Utilisez les boutons pour charger et sauvegarder des images :
    - **Charger une image** : Ouvre une boîte de dialogue pour sélectionner une image au format ULBMP.
    - **Enregistrer l'image** : Ouvre une boîte de dialogue pour sélectionner la version et les options de sauvegarde de l'image.

## Structure du projet

- `main.py` : Point d'entrée de l'application.
- `window.py` : Contient la classe `MainWindow` qui gère l'interface utilisateur.
- `image.py` : Contient la classe `Image` qui représente une image.
- `encoding.py` : Contient les classes `Encoder` et `Decoder` pour l'encodage et le décodage des images au format ULBMP.
- `pixel.py` : Contient la classe `Pixel` qui représente un pixel d'image.
