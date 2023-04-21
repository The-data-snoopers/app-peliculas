from collections import Counter
import unicodedata
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
import pandas as pd
import nltk
import enchant
import re


class Limpieza(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
        #self.palabras_no_existe = []


    def fit(self, X, y=None):
        print("Fit...")
        return self

    def transform(self, X, y=None):
        print("Transform...")
        return self.preprocess(X)

   

    def remove_words(self,text):
        
        en_us = enchant.Dict("en_US")
        es_es = enchant.Dict("es_ES")
        palabras_no_existe = []
        for word in text.split(" "):
            if en_us.check(word)== False and es_es.check(word) == False:
                if word not in palabras_no_existe:
                    palabras_no_existe.append(word)

        regex = r'\b(' + '|'.join(palabras_no_existe) + r')\b'
        texto_sin_palabras_raras = re.sub(regex, '', text)

        return texto_sin_palabras_raras

    def preprocess(self, df:pd.DataFrame) -> pd.DataFrame:
        print("Preprocessing text...")
        # convert series to dataframe
        movies_df = pd.DataFrame(df)


        # Descargando las stopwords
        nltk.download('stopwords')
        stop_words = list(stopwords.words('spanish'))
        stop_words_e = list(stopwords.words('english'))

        # Eliminando caracteres no alfanumericos y pasamos los caracteres a minusculas
        movies_df['review_es'] = movies_df['review_es'].apply(lambda x: re.sub(r'\W+', ' ', x).lower())

        # Eliminamos las stopwords de español y ingles
        movies_df['review_es'] = movies_df['review_es'].apply(lambda x: " ".join([word for word in x.split() if word not in stop_words]))
        movies_df['review_es'] = movies_df['review_es'].apply(lambda x: " ".join([word for word in x.split() if word not in stop_words_e]))

        #Eliminamos las palabras que no pertenecen al Español ni Inglés
        #movies_df['review_es'] = movies_df['review_es'].apply(lambda x: self.remove_words(x))
        

        #Remover las palabras con poca frecuencia de apariciones
        word_count = Counter()
        for text in movies_df['review_es']:
            for word in text.split():
                word_count[word] += 1
        RARE_WORDS = set(word for (word, wc) in word_count.most_common()[:-10:-1])
        movies_df['review_es'] = movies_df['review_es'].apply(lambda x: " ".join([word for word in x.split() if word not in RARE_WORDS]))

        # Remover las palabras con alta frecuencia de apariciones
        FREQUENT_WORDS = set(word for (word, wc) in word_count.most_common(10))  
        movies_df['review_es']= movies_df['review_es'].apply(lambda x: " ".join([word for word in x.split() if word not in FREQUENT_WORDS]))
        
        # Eliminamos las tildes
        movies_df['review_es'] = movies_df['review_es'].apply(lambda x: ''.join(c for c in (unicodedata.normalize('NFD', x)) if unicodedata.category(c) != 'Mn'))
        movies = movies_df['review_es']
        print("Termino")


        return movies