import inspect
import argparse
import modules

import os
from os import listdir
from os.path import isfile, join

def main():
    """Exécute l'algorithme principale pour générer les exercices demandés."""

    # déclare le chemin vers les modules à importer
    path = './modules/'

    # déclare les headers à filtrer de la liste des exercices existants
    headers = ['__init__', 'fonctions']

    # déclare les arguments de commande
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', 
                        help='type of exercise to generate \"conjugaison\" or \"fillblanks\" or \"scramble\"  or \"questions\" or \"all\"', 
                        type=str, 
                        default='NA')
    parser.add_argument('--subtitle', 
                        help='source subtitle file to use to generate exercises"', 
                        type=str, 
                        default='NA')
    parser.add_argument('--textfile', 
                        help='source text file to use to generate exercises"', 
                        type=str, 
                        default='NA')
    args = parser.parse_args()

    # déclare la liste des exercices existants par nom des classes correspondantes
    exercices = [
        os.path.splitext(m)[0] 
        for m in listdir(path) 
        if isfile(join(path, m)) and os.path.splitext(m)[0] not in headers
        ]

    # teste si le type d'exercice entré par l'utilisateur est connu
    if args.generate in exercices:
        # si oui, instancie la classe correspondante
        classe = __import__('modules.' + args.generate, fromlist=[args.generate.title()])
        instance = getattr(classe, args.generate.title())()
        # et appelle la méthode d'exécution
        instance.run(args.subtitle, args.generate)

    else:
        # si non, renvoie une erreur texte
        print(exercices)
        raise NameError('Type d\'exercice non reconnu')

    return

main()