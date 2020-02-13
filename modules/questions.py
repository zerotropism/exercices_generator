import spacy
import names
import pathlib
import numpy as np
import pandas as pd

import gender_guesser.detector as gender

import gensim
from gensim.models import KeyedVectors
from gensim.scripts.glove2word2vec import glove2word2vec

import nltk
from nltk.stem.wordnet import WordNetLemmatizer

from modules.fonctions import Fonctions
F = Fonctions()


class Questions():
    """Rassemble les méthodes des exercices de type 'questions'."""

    # déclare les attributs de classe
    nlp = spacy.load('en')
    gender_detector = gender.Detector()

    def name(self):
        return "Questions"

    def ensureUtf(self, s):
        """S'assure que le paramètre passé est bien encodé en utf-8."""

        try:
            if type(s) == unicode:
                return s.encode('utf8', 'ignore')
        except: 
            return str(s)

    def get_tense(self, tag):
        """Détermine le mode du verbe conjugué en fonction du postag."""

        infinitive = ['VB']
        present = ['VBG', 'VBP', 'VBZ']
        past = ['VBD', 'VBN']
        
        tense = ''
        if tag in infinitive:
            tense = 'INFINITIVE'
        elif tag in present:
            tense = 'PRESENT'   
        elif tag in past:
            tense = 'PAST'
        else:
            tense = 'NA'

        return tense

    def question_word(self, text):
        """Détermine le label du mot en fonction du postag."""

        doc = self.nlp(text)
        label = ''
        if(doc.ents):
            label = doc.ents[0].label_
        else:
            label = 'NA'
        
        # déclare les listes de labels possibles
        who = ['PERSON']
        where = ['GPE', 'LOC']
        when = ['DATE', 'TIME']
        how_many = ['PERCENT', 'MONEY', 'QUANTITY', 'CARDINAL']
        what = ['NORP', 'FAC', 'ORG', 'PRODUCT', 'EVENT', 'WORK_OF_ART', 'LAW', 'LANGUAGE', 'ORDINAL', 'CARDINAL']

        # teste le mot
        question_word = ''
        if label in who:
            question_word = 'Who'
        elif label in what:
            question_word = 'What'
        elif label in where:
            question_word = 'Where'
        elif label in how_many:
            question_word = 'How many'
        elif label in when:
            question_word = 'When'
        else:
            question_word = 'What'

        return question_word

    def auxiliary_verb(self, verb, tense, number):
        """Détermine la conjugaison de l'auxiliaire en fonction :
            - du mode,
            - du nombre et
            - du verbe.
        """

        auxiliary_verb = ''
        # teste le mode
        if tense == 'PRESENT':
            # teste le verbe
            if verb == 'be':
                # teste le nombre
                if number == 'SG':
                    auxiliary_verb = 'is'
                else:
                    auxiliary_verb = 'are'
            else:
                if number == 'SG':
                    auxiliary_verb = 'does'
                else:
                    auxiliary_verb = 'do'
        elif tense == 'PAST':
            if verb == 'be':
                if number == 'SG':
                    auxiliary_verb = 'was'
                else:
                    auxiliary_verb = 'were'
            else:
                auxiliary_verb = 'did'
        elif tense == 'FUTURE':
            auxiliary_verb = 'will'
        else:
            auxiliary_verb = 'NA'

        return auxiliary_verb
    
    def generate_names(self, name):
        """Détermine le genre d'un nom."""

        # déclare le détecteur de genre
        gender = self.gender_detector.get_gender(self.ensureUtf(name))
        list_names = [name]
        # teste le genre
        if gender == 'male':
            list_names.extend([names.get_full_name(gender='male') for x in range(3)])
        else:
            list_names.extend([names.get_full_name(gender='female') for x in range(3)])

        return list_names
    
    def generate_words(self, string):
        """Génère des mots similaires par proximité vectorielle en base du gloVe n-dimensions."""

        # déclare le dataset gloVe à n-dimensions
        glove_file = 'data/sampled_glove.6B.50d.txt'
        word2vec_file = 'data/sampled_word2vec-glove.6B.50d.txt'
        file = pathlib.Path(word2vec_file)

        # teste son existence dans les dossiers
        if file.exists():
            # s'il existe, pas besoin de le générer à nouveau
            print('word2vec_file {} already exists, loading existing one, not generated'.format(word2vec_file))
        else:
            # si non, le génère
            print('word2vec_file {} doesn\'t exist, generating new one'.format(word2vec_file))
            glove2word2vec(glove_file, word2vec_file)

        # déclare le modèle
        model = KeyedVectors.load_word2vec_format(word2vec_file)

        # déclare la liste des stopwords à filtrer
        spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
        word = ''
        string_splitted = string.split()

        # sépare mot par mot, nécessaire dans le cas de beaucoup de mots dans l'input str
        for i in range(len(string_splitted)):
            if(string_splitted[i].lower() not in spacy_stopwords):
                word = string_splitted[i]

        # récupère les 100 premiers mots les plus similaires par proximité vectorielle
        list_words = []
        if word != '':
            try:
                list_words = model.most_similar(positive=[word], topn=100)
            except:
                list_words = []

        # défini les premiers mots de la liste
        list_close_words = [word]
        list_far_words = [word]

        # récupère les 4 réponses du QCM (une ou plusieurs réponses correctes)
        count = 0
        for i in range(len(list_words)):
            if word not in list_words[i][0]:
                list_close_words.append(list_words[i][0])
                count = count + 1
            if count == 3:
                break

        list_words.reverse()

        # récupère les 4 réponses du QCU (une seule réponse correcte)
        count = 0
        i = 0
        for i in range(len(list_words)):
            if word not in list_words[i][0]:
                list_far_words.append(list_words[i][0])
                count = count + 1
            if count == 3 :
                break
        
        dict_words = {}
        dict_words['list_far_words'] = list_far_words
        dict_words['list_close_words'] = list_close_words

        return dict_words

    def tokenize_sentences(self, paragraph):
        """
        """


        lemmatizer = WordNetLemmatizer()
        self.nlp.add_pipe(self.nlp.create_pipe('merge_noun_chunks'))
        doc = self.nlp(self.ensureUtf(paragraph))

        dict_sentences = {}
        dict_sentences['sent'] = []
        dict_sentences['sent_postags'] = []

        for sent in doc.sents:
            doc2 = self.nlp(sent.text.replace(u'\xa0', u'').replace('-', ' '))  
            
            dict_sentences['sent'].append(sent.text.replace(u'\xa0', u'').replace('-', ' '))

            dict_postag = {}
            dict_postag['text'] = []
            dict_postag['pos'] = []
            dict_postag['tag'] = []
            dict_postag['dep'] = []

            dict_postag['patterns_text'] = []
            dict_postag['patterns_label'] = []
            dict_postag['patterns_question_word'] = []
            dict_postag['patterns_pos'] = []
            dict_postag['patterns_tag'] = []
            dict_postag['patterns_dep'] = []
            dict_postag['patterns_aux'] = []
            dict_postag['patterns_verb'] = []

            current_pattern_text = []
            current_pattern_label = []
            current_pattern_question_word = []
            current_pattern_pos = []
            current_pattern_tag = []
            current_pattern_dep = []
            current_pattern_aux = []
            current_pattern_verb = []
            
            for elem in doc2:
                dict_postag['text'].append(elem.text)
                dict_postag['pos'].append(elem.pos_)
                dict_postag['tag'].append(elem.tag_)
                dict_postag['dep'].append(elem.dep_)

                if elem.dep_ == 'ROOT':
                    current_pattern_aux.append(self.auxiliary_verb(lemmatizer.lemmatize(elem.text, 'v'), self.get_tense(elem.tag_), 'SG'))
                    current_pattern_verb.append(lemmatizer.lemmatize(elem.text, 'v'))
                else:
                    current_pattern_aux.append('')
                    current_pattern_verb.append('')

                if elem.dep_ != '' and elem.dep_ != 'punct' :
                    current_pattern_text.append(elem.text)
                    doc3 = self.nlp(elem.text)
                    
                    if doc3.ents:
                        current_pattern_label.append(doc3.ents[0].label_)
                        current_pattern_question_word.append(self.question_word(doc3.ents[0].label_))
                    else:
                        current_pattern_label.append('')
                        current_pattern_question_word.append('')

                    current_pattern_pos.append(elem.pos_)
                    current_pattern_tag.append(elem.tag_)
                    current_pattern_dep.append(elem.dep_) 

                if elem.dep_ == 'punct' :
                    dict_postag['patterns_text'].append(current_pattern_text)
                    dict_postag['patterns_label'].append(current_pattern_label)
                    dict_postag['patterns_question_word'].append(current_pattern_question_word)
                    dict_postag['patterns_pos'].append(current_pattern_pos)
                    dict_postag['patterns_tag'].append(current_pattern_tag)
                    dict_postag['patterns_dep'].append(current_pattern_dep)
                    dict_postag['patterns_aux'].append(current_pattern_aux)
                    dict_postag['patterns_verb'].append(current_pattern_verb)
                    
                    current_pattern_text = []
                    current_pattern_label = []
                    current_pattern_question_word = []
                    current_pattern_pos = []
                    current_pattern_tag = []
                    current_pattern_dep = []
                    current_pattern_aux = []
                    current_pattern_verb = []
                    
            dict_sentences['sent_postags'].append(dict_postag)

        return dict_sentences

    def questions(self, paragraph):
        """Méthode principale :
        
        Compile les questions à passer en paramètres pour créer les trois types d'exercices :
        - question ouverte,
        - qcm,
        - qcu.
        """
        
        dict_sentences = self.tokenize_sentences(paragraph)

        dict_qna = {}
        dict_qna['text'] = []
        dict_qna['questions_open'] = []
        dict_qna['answers_open'] = []
        dict_qna['questions_qcm'] = []
        dict_qna['answers_qcm'] = []
        dict_qna['questions_qcu'] = []
        dict_qna['answers_qcu'] = []

        for i in range(len(dict_sentences['sent'])):
            
            for j in range(len(dict_sentences['sent_postags'][i]['patterns_dep'])):
                
                if 'nsubj' in dict_sentences['sent_postags'][i]['patterns_dep'][j]:
                    nsubj_pos = dict_sentences['sent_postags'][i]['patterns_dep'][j].index('nsubj')
                    root_pos = nsubj_pos + 1

                    if root_pos < len(dict_sentences['sent_postags'][i]['patterns_dep'][j]):
                        if dict_sentences['sent_postags'][i]['patterns_dep'][j][root_pos] == 'ROOT':
                            dict_qna['text'].append(' '.join(dict_sentences['sent_postags'][i]['patterns_text'][j]))
                            rest = ''
                        
                            for k in range(root_pos, len(dict_sentences['sent_postags'][i]['patterns_text'][j])):
                                rest = rest + ' ' + dict_sentences['sent_postags'][i]['patterns_text'][j][k]

                            question = self.question_word(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]) + rest + ' ?' 
                            dict_qna['questions_open'].append(question)
                            answer = dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]
                            dict_qna['answers_open'].append(answer)

                            if(dict_sentences['sent_postags'][i]['patterns_label'][j][nsubj_pos] == 'PERSON'):
                                question = self.question_word(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]) + rest + ' ?' 
                                dict_qna['questions_qcm'].append(question)
                                answer = dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]
                                dict_qna['answers_qcm'].append(self.generate_names(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]))

                                question = self.question_word(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]) + rest + ' ?' 
                                dict_qna['questions_qcu'].append(question)
                                answer = dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]
                                dict_qna['answers_qcu'].append(self.generate_names(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]))

                            else:
                                my_dict_answers = self.generate_words(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos])
                                
                                question = self.question_word(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]) + rest + ' ?' 
                                dict_qna['questions_qcm'].append(question)
                                answer = dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]
                                dict_qna['answers_qcm'].append(my_dict_answers['list_close_words'])

                                question = self.question_word(dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]) + rest + ' ?' 
                                dict_qna['questions_qcu'].append(question)
                                answer = dict_sentences['sent_postags'][i]['patterns_text'][j][nsubj_pos]
                                dict_qna['answers_qcu'].append(my_dict_answers['list_far_words'])

        return dict_qna
    
    def create_open_questions(self, dict_qna):
        """Génère des questions ouvertes."""

        prefinal = np.column_stack((dict_qna['text'], dict_qna['questions_open'], dict_qna['answers_open']))
        final = pd.DataFrame(prefinal, columns=['Phrase', 'Question', 'Answer'])

        return final

    def create_qcm(self, dict_qna):
        """Génère des questions à plusieurs réponses correctes simultanées possibles."""

        prefinal = np.column_stack((dict_qna['text'], dict_qna['questions_qcm'], dict_qna['answers_qcm']))
        final = pd.DataFrame(prefinal, columns=['Phrase', 'Question', 'Answers'])

        return final

    def create_qcu(self, dict_qna):
        """Génère des questions à une seule réponse correcte possible."""

        prefinal = np.column_stack((dict_qna['text'], dict_qna['questions_qcu'], dict_qna['answers_qcu']))
        final = pd.DataFrame(prefinal, columns=['Phrase', 'Question', 'Answers'])

        return final

    def run(self, subs, exo):
        """Méthode d'exécution."""

        # appelle la méthode commune de conversion de .srt vers .txt
        texte = F.srt_to_text(subs)
        # appelle la méthode principale locale 
        dico = self.questions(texte)
        # puis la méthode d'exercice de questions ouvertes
        dataframe_open = self.create_open_questions(dico)
        F.write_csv(dataframe_open, subs, exo + '_open')

        # puis celle de QCM
        dataframe_qcm = self.create_qcm(dico)
        F.write_csv(dataframe_qcm, subs, exo + '_qcm')

        # puis celle de QCU
        dataframe_qcu = self.create_qcu(dico)
        F.write_csv(dataframe_qcu, subs, exo + '_qcu')

        return