import re
import os
import sys
import pandas as pd
from pathlib import Path
from inspect import currentframe


class Fonctions():
    """Rassemble toutes les méthodes communes."""

    def name(self):
        return "Fonctions"

    def srt_to_list(self, subtitle):
        """Prend un sous-titre au format '.srt' en entrée et retourne une liste de phrases."""

        # ouvre un fichier et déclare sa variable
        file = open(subtitle, "r")
        lines = file.readlines()
        file.close()

        # nettoie les sous-titres et les transforme en chaîne de caractères
        text = []
        for line in lines:
            if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
                if line[0].isalpha() & line[0].islower():
                    text = [word.strip() for word in text]
                    text[-1] = text[-1] + ' ' + line
                else:
                    text.append(line)
        text = [word.strip() for word in text]
        return text

    def srt_to_text(self, subtitle):
        """Prend un sous-titre au format '.srt' en entrée et retourne une phrase en texte brut."""

        # ouvre un fichier et déclare sa variable
        file = open(subtitle, "r")
        lines = file.readlines()
        file.close()

        # nettoie les sous-titres et les transforme en chaîne de caractères
        text = []
        for line in lines:
            if re.search('^[0-9]+$', line) is None and re.search('^[0-9]{2}:[0-9]{2}:[0-9]{2}', line) is None and re.search('^$', line) is None:
                if line[0].isalpha() & line[0].islower():
                    text = [word.strip() for word in text]
                    text[-1] = text[-1] + ' ' + line
                else:
                    text.append(line)
        text = [word.strip() for word in text]
        # joint tous le texte au format brut
        text = ' '.join(text)
        return text

    def write_xlsx(self, pandasDF, fileName, exerciceType):
        """Prend un dataframe pandas en entrée et enregistre un fichier au format '.xlsx' au chemin souhaité et en respectant la typologie des titres."""

        outputXLSXFilesPath = 'exercices'

        fileNameBaseName = os.path.basename(fileName)
        fileNameInt = os.path.splitext(fileNameBaseName)[0]
        myExcelFile = outputXLSXFilesPath + '/' + fileNameInt + '_exercice_' + exerciceType + '.xlsx'

        dirNameInt = os.path.dirname(myExcelFile)
        if not os.path.exists(dirNameInt):
            os.makedirs(dirNameInt)

        writer = pd.ExcelWriter(myExcelFile)
        pandasDF.to_excel(writer, 'Sheet1')
        writer.save()

        my_file = Path(myExcelFile)
        if my_file.is_file():
            print('File: ' + myExcelFile + ' created.')
        else:
            print('File: ' + myExcelFile + ' NOT created, please check what is wrong!!!')
            sys.exit(1)

    def write_csv(self, _dataframe, _filename, _exercise):
        """Prend un dataframe pandas en entrée et enregistre un fichier au format '.csv' au chemin souhaité et en respectant la typologie des titres."""

        basename = os.path.basename(_filename)
        rootname = os.path.splitext(basename)[0]
        filetitle = 'exercices/' + rootname + '_exercice_' + _exercise + '.csv'

        dirname = os.path.dirname(filetitle)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        _dataframe.to_csv(filetitle, sep=',', encoding='utf-8', index=False)

        filepath = Path(filetitle)
        if filepath.is_file():
            print('File: ' + filetitle + ' created.')
        else:
            print('File: ' + filetitle + ' NOT created, please check what is wrong!!!')
            sys.exit(1)

    def text_from_file(self, textfile):
        """Prend un fichier en entrée et en extrait le texte."""

        with open(textfile, 'r') as file:
            data = file.read().replace('\n', '')
        
        return data

    def get_linenumber(self):
        """Détermine le numéro de ligne du tableau du caller."""

        cf = currentframe()
        return cf.f_back.f_lineno


class Modes():
    """Tableau de conversion entre les postag nltk et la nomenclature des modes de mlconjug."""

    modes = {
        'VB': {
            'mode': 'imperative',
            'temps': 'imperative present',
            'personne': '2s'
        },
        'VBD': {
            'mode': 'indicative',
            'temps': 'indicative past tense',
            'personne': '1s'
        },
        'VBG': {
            'mode': 'indicative',
            'temps': 'indicative present continuous',
            'personne': '1s 1s'
        },
        'VBN': {
            'mode': 'indicative',
            'temps': 'indicative present perfect',
            'personne': '1s'
        },
        'VBP': {
            'mode': 'indicative',
            'temps': 'indicative present',
            'personne': '1s'
        },
        'VBZ': {
            'mode': 'indicative',
            'temps': 'indicative present',
            'personne': '3s'
        }
    }