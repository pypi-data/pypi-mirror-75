import pandas as pd
import numpy as np
from io import StringIO
import seaborn as sns
import hashlib
import re #cuenta con funciones para trabajar con expresiones regulares y cadenas.
import string
import os
from time import time
import nltk
import gensim
import spacy
import es_core_news_sm
from spacy import displacy
from nltk.corpus import stopwords
from gensim import corpora
from pprint import pprint

from datup.anonymization.data_io_anonymization import (
    variables_pii,
    concatenar,
    concatenar_id,
    organizar,
    profiling,
    normalize,
    observaciones,
    organizar_observaciones,
    eliminar_duplicados
)

def eliminacion (df):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            df1: DataFrame
                It is the DataFrame with which want to work

        :rtype: DataFrame
        :return: Returns a dataframe with an analysis of data type information, application of reengineering techniques, profiling,
        automatic recognition of personal identification variables, application of concatenation of personal identification variables,
        elimination of personal identification variables, application of elimination of names own and personally identifiable data
        for unstructured data to a column named 'Observaciones'. Appearance of a column named 'Puntajes' that allows giving a score to
        each cell of the 'Observaciones' field depending on whether or not it has personal identification data.

        Puntajes = 1
        (It has variables of personal identification)
        Puntajes = -1
        (Does not have personal identification variables)

        Examples
        --------
        >>> import datup as dt
        >>> dt.eliminacion (df)
        '''
        df.head()
        df1=df.copy()

        #Profiling
        profiling(df1)

        #REINGENIERIA
        columnas=df1.columns
        ctd_columnas=len(columnas)
        df1=df1.fillna('No disponible')
        df1=df1.astype(str).apply(lambda x: x.str.upper())

        #Profiling
        profiling(df1)

        #IDENTIFICACION DE VARIABLES PII---------------------------------------------------
        columnas=df1.columns
        ctd_columnas=len(columnas)
        print("La variables de identificación personal de este conjuntos de datos son: ")
        individuo=variables_pii() #Lista de nombre de variables de identificacion personal
        id_persona=list()
        inicio=0

        while (inicio <= (ctd_columnas-1)) :
            for inter in individuo.general1:
                if (re.findall(inter,normalize(columnas[inicio].lower()))):
                        id_persona.append(columnas[inicio])
            inicio+=1
        id_persona=eliminar_duplicados(id_persona)
        print(id_persona)
        print("La variables de identificación personal a concatenar son: ")
        id_persona_concat=concatenar_id(id_persona)
        print(id_persona_concat)


        #ELIMINACION DE VARIABLES----------------------------
        if (len(id_persona)>0):
            df3=df1.copy()
            inicio=0
            while(inicio<=(len(id_persona)-1)):
                df3.drop(id_persona[inicio],axis='columns',inplace=True)
                inicio+=1
            df3.head()

            df3.head()
        #----------------------NPL----------------------------
            df4=df3.copy()
            obser=observaciones(df4)
            if(len(observaciones(df4))>0):
                nlp = es_core_news_sm.load() #idioma español


                #Texto tipo Titulo
                df4=df4.astype(str).apply(lambda x: x.str.title())

                #quitar mayusculas
                df4['Mayusculas']= df4[observaciones(df4)]. apply (lambda x: " " .join (x.lower () for x in x.split ()))

                #quitar puntuaciones
                df4['Puntuaciones'] = df4['Mayusculas'].str.replace('[^\w\s]','')

                #quitar palabras vacias(articulos, conectores, etc)
                stop = stopwords.words('spanish')
                df4['Stop_words'] = df4['Puntuaciones'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))


                #tokenizacion
                df4['Token'] = df4['Stop_words'].apply(lambda x: nlp.tokenizer(x))

                #cantidad de tokens
                df4['num_tokens'] = [len(token) for token in df4.Token]

                #aplicar nlp - reconocimiento de entidades
                df4['NER'] = df4['Stop_words'].apply(lambda x: str(nlp(x).ents))


                inicio=0
                #------------------------------------------------------------------------
                # reconocmineto de personas
                while(inicio<=len(df4.index)-1):
                    doc = nlp(df4.loc[inicio,'Stop_words']) #analisis de palabras claves
                    for word in doc.ents:
                        if (word.label_=='PER'): #comparacion de los label de tipo persona
                            df4.loc[inicio,'Nombres_Observacion']=word.text
                            df4.loc[inicio,'Puntajes']=1
                    inicio+=1

                #rellenar los valores vacios
                df4['Puntajes'].replace(np.nan,-1, inplace=True)
                df4['Nombres_Observacion'].replace(np.nan,'No disponible', inplace=True)

                #eliminacion de columnas del NPL
                datos=[]
                inicio1=0
                ctd_row=len(df4.index)
                while (inicio1<=ctd_row-1):
                    if (re.findall(df4['Nombres_Observacion'][inicio1],df4['Puntuaciones'][inicio1])):
                        datos.append(df4['Puntuaciones'][inicio1].replace(df4['Nombres_Observacion'][inicio1],""))

                    else:
                        datos.append(df4['Puntuaciones'][inicio1])
                    inicio1+=1

                #Generacion del dataframe con el campo de observaciones con la PII eliminada
                df_datos = pd.DataFrame(datos, columns =['Observacion_PII_eliminada'])

                df4['Observacion_PII_eliminada']=df_datos

                df5=df4.copy()

                #Organizar el dataset para dejarlos con el campo de observaciones anonimizado y el campo de reconocimiento automatico
                #de variables PII

                df5.drop([obser,'Mayusculas','Puntuaciones','Stop_words','Token','num_tokens','NER','Nombres_Observacion'], axis='columns',inplace=True)

                #Organizar el campo de obsevaciones
                df5=organizar_observaciones (df5)
                return (df5)
            else:
                return (df3)

        else :
            print('Esta Archivo no tiene variables de identificación personal')
    except eliminacion as error:
        print(error)
