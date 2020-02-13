import numpy as np
import pandas as pd
from random import shuffle

from modules.fonctions import Fonctions
F = Fonctions()


class Scramble():
    """Rassemble les méthodes des exercices de type 'scramble'."""

    def name(self):
        return "Scramble"

    def scramble(self, sent):
        """Méthode principale :
        
        Mélange tous les mots d'une phrase reçue.
        """
        
        # mélange les mots d'une phrase
        l = []
        for s in sent:
            split = s.split()
            shuffle(split)
            s = ' '.join(split)
            l.append(s)
        
        m = []
        for s in l:
            split = s.split()
            m.append(split)    
        
        prefinal = np.column_stack((l, m, sent))
        final = pd.DataFrame(prefinal, columns=['Phrase', 'Scramble', 'Answer'])

        return final

    def run(self, subs, exo):
        """Méthode d'exécution."""

        # appelle la méthode commune de conversion de .srt vers type <list>
        texte = F.srt_to_list(subs)
        # appelle la méthode principale locale
        dataframe = self.scramble(texte)
        # retourne la méthode commune de génération de .csv
        return F.write_csv(dataframe, subs, exo)