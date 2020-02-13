import sys
import inspect

import os
from os import listdir
from os.path import isfile, join


class All():
    """Exécute toutes les méthodes d'exécution de tous les types d'exercices existants."""

    def name(self):
        return "All"

    def run(self, subs, exo):
        """Méthode principale :
        
        Appelle toutes les méthodes d'exécution précédentes.
        """

        # déclare les variables de chemin et modules à ne pas tenir en compte
        path = './modules'
        headers = ['__init__', 'fonctions']
        
        # appelle tous les modules nécessaires à l'appel des classes d'exercice
        modules = [
            os.path.splitext(m)[0] 
            for m in listdir(path) 
            if isfile(join(path, m)) 
            and os.path.splitext(m)[0] not in headers 
            and os.path.splitext(m)[0] != self.name().lower()
            ]

        # appelle toutes les instances exceptée "All()" en liste             
        instances = [
            getattr(__import__('modules.' + module, fromlist=[module.title()]), module.title())()
            for module in modules
            ]

        # appelle toutes les méthodes d'exécution
        for instance in instances:
            instance.run(subs, exo)
        
        return