import numpy as np
import pandas as pd

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

from modules.fonctions import Fonctions
from modules.fonctions import Modes
F = Fonctions()
M = Modes()


class Conjugaison():
    """Rassemble les méthodes des exercices de type 'conjugaison'."""

    def name(self):
        return "Conjugaison"

    def infinitive(self, word):
        """Génère l'infinitif d'un verbe."""

        # en anglais
        lemmatizer = WordNetLemmatizer()
        verb = lemmatizer.lemmatize(word, 'v')
        return str(verb)

    def conjugaison(self, sent):
        """Méthode principale :

        Génère une phrase avec un verbe manquant depuis un sous-titre reçu dont l'élève doit retrouver la bonne conjugaison sans propositions.
        """
        
        ext = ["'s", "'re", "is", "are", "'ve", "'m", "am"]

        # cherche le verbe dans le texte en postagant avec nltk
        p = []
        for s in sent:
            token = nltk.word_tokenize(s)
            pos = nltk.pos_tag(token)
            p.append(pos)
        
        # créer une liste de verbes postagués
        f = []
        for i in range(0, len(p)):
            for l in range(0, len(p[i])): 
                if p[i][l][1] in M.modes.keys():
                    f.append(p[i][l])
       
        # retire les doublons par un set()
        g = []
        for i in range(len(f)):
            if f[i][0] in ext:
                continue
            else:
                g.append(f[i])
        g = dict(set(g))

        # créé un tableau avec le dialogue, le verbe à l'infinitif et la réponse
        dialog = []
        answer = []
        verb_inf = []
        for s in sent:
            for w in g.keys():
                if w in s:
                    m = s.replace(w,' ___________ ')
                    dialog.append(m)
                    answer.append(w)
                    verb_inf.append("to " + self.infinitive(w))
        
        prefinal = np.column_stack((dialog, verb_inf, answer))
        final = pd.DataFrame(prefinal, columns=['Phrase', 'Verb', 'Answer'])
        
        return final
    
    def run(self, subs, exo):
        """Méthode d'exécution"""

        # appelle la méthode commune de conversion de .srt vers type <list>
        liste = F.srt_to_list(subs)
        # appelle la méthode principale locale
        dataframe = self.conjugaison(liste)
        # retourne la méthode commune de génération de .csv
        return F.write_csv(dataframe, subs, exo)