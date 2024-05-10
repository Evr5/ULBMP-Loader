#!/usr/bin/env python3

import argparse
import os.path
from sys import argv

from pixel import Pixel
from image import Image
from encoding import *

import PIL.Image
import numpy as np

"""
Attention PIL et numpy sont requis !
Vous pouvez les installer avec la commande suivante :
$ python3 -m pip install numpy Pillow
"""

PROGRAM_NAME = os.path.splitext(os.path.relpath(argv[0]))[0]

def load_params():
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description='Convertisseur d\'images vers le format ULBMP 1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=
f'''Exemple d\'utilisation pour convertir le fichier house.tiff au format ULBMP:
    $ ./{PROGRAM_NAME} house.tiff house.ulbmp
Si house.ulbmp existe déjà mais que vous voulez le remplacer :
    $ ./{PROGRAM_NAME} --force house.tiff house.ulbmp
'''
    )
    parser.add_argument(
        'src',
        help='Nom du fichier d\'entrée'
    )
    parser.add_argument(
        'dest',
        help='Nom du fichier de sortie'
    )
    parser.add_argument(
        '--force', required=False,
        action='store_true',
        help='Force l\'écriture du fichier de destination, même s\'il existe déjà'
    )
    return parser.parse_args()

def get_nb_channels(img):
    return np.asarray(img).shape[2]

def main():
    params = load_params()
    if not os.path.isfile(params.src):
        raise ValueError('Le fichier donné en entrée n\'existe pas.')
    if os.path.isfile(params.dest) and not params.force:
        raise ValueError('Le fichier de sortie existe déjà. Utilisez `--force` pour l\'écraser.')
    pil_img = PIL.Image.open(params.src)     # on lit l'image avec PIL
    if get_nb_channels(pil_img) != 3:        # Si il y a un canal alpha
        pil_img = pil_img.convert('RGB')     # on convertit en RGB classique
    if get_nb_channels(pil_img) != 3:
        raise ValueError(f'Nombre de canaux inattendu : {get_nb_channels(pil_img)}')
    w, h = pil_img.size                      # on récupère ses dimensions
    pixels = [                               # On convertit en instances de Pixel
        Pixel(*pil_img.getpixel((x, y))) \
        for y in range(h) for x in range(w)
    ]
    ulbmp_img = Image(w, h, pixels)          # On crée l'instance de Image associée
    Encoder(ulbmp_img).save_to(params.dest)  # Et finalement on sauve en ULBMP 1

if __name__ == '__main__':
    main()
