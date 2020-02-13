# imports
import re
import numpy as np
import pandas as pd

import nltk
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from mlconjug import Conjugator

from modules.fonctions import Fonctions
from modules.fonctions import Modes
F = Fonctions()
M = Modes()


class Fillblanks():
    """Rassemble les méthodes des exercices de type 'fillblanks'."""

    def name(self):
        return "Fillblanks"
    
    def fill(self, word, postag):
        """Teste et attribue la conjugaison correspondante au verbe en fonction du postag."""

        # déclaration
        conjugator = Conjugator(language='en')

        # teste si le paramètre postag appartient aux postags nltk
        if postag in M.modes.keys():
            # si oui, attribue la conjugaison correspondante
            mode = M.modes[postag]
            verb = conjugator.conjugate(word).conjug_info[mode['mode']][mode['temps']][mode['personne']]
        else:
            # sinon  attribue le str 'no_tag'
            verb = 'no_tag'
        
        return str(verb)

    def fillblanks(self, sent):
        """Méthode principale :
        
        Génère une phrase avec un verbe manquant depuis un sous-titre reçu dont l'élève doit trouver le bon verbe parmis d'autres.
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
                if p[i][l][1] in list(M.modes.keys()):
                    f.append(p[i][l])

        # retire les doublons par un set()
        g = []
        for i in range(len(f)):
            if f[i][0] in ext:
                continue
            else:
                g.append(f[i])
        g = dict(set(g))
    
        # créé les phrases avec les blancs
        ans = []
        fill = []
        for s in sent:
            for w in g.keys():
                if w in s:
                    m = s.replace(w,' ___________ ')
                    fill.append(m)
                    ans.append(w)
        prefinal = np.column_stack((fill,ans))
        prefinal = pd.DataFrame(prefinal, columns=['Phrase', 'Answer'])
        
        answers = pd.DataFrame(prefinal.iloc[:,1])
        answers['2'] = None
        answers['3'] = None
        answers['4'] = None
        
        # itère toutes les réponses, 
        # identifie le postag depuis le set g[] et 
        # lui assigne les synonymes
        stem = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        for i in range(len(answers)):
            synonyms = [] 
            antonyms = []
            
            word = answers.iloc[i,0]
            word_tag= g[word]
            
            # identifie les synonymes et antonymes de chaque mot
            for syn in wordnet.synsets(word): 
                for l in syn.lemmas():
                    p1 = re.compile('[A-Za-z]+_[A-Za-z]+')
                    p2 = re.compile('[A-Za-z]+_[A-Za-z]+_[A-Za-z]+')
                    p3 = re.compile('[A-Za-z]+_[A-Za-z]+_[A-Za-z]+_[A-Za-z]+')
                    p4 = re.compile('[A-Za-z]+-[A-Za-z]+-[A-Za-z]+')
                    
                    if any([
                        re.match(l.name(), word, re.IGNORECASE),
                        re.match(word, l.name(), re.IGNORECASE),
                        l.name() == stem.stem(word),
                        l.name() == lemmatizer.lemmatize(word, 'v'),
                        p1.match(l.name()),
                        p2.match(l.name()),
                        p3.match(l.name()),
                        p4.match(l.name())
                    ]):
                        continue
                    synonyms.append(l.name())

                    if l.antonyms():
                        antonyms.append(l.antonyms()[0].name()) 
            
            # teste si la liste des synonymes est non nulle
            if len(synonyms) != 0:
                answers.iloc[i,1] = self.fill(synonyms[0], word_tag)
                answers.iloc[i,2] = self.fill(synonyms[1], word_tag)
            else:
                continue
        
        # concatène les réponses dans un data frame
        final = np.column_stack((prefinal, answers))
        final = pd.DataFrame(final, columns=['Phrase', 'Answer', '1', '2', '3', '4'])
                
        return final

    def run(self, subs, exo):
        """Méthode d'exécution."""

        # appelle la méthode commune de conversion de .srt vers type <list>
        liste = F.srt_to_list(subs)
        # appelle la méthode principale locale
        dataframe = self.fillblanks(liste)
        # retourne la méthode commune de génération de .csv
        return F.write_csv(dataframe, subs, exo)