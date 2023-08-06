import pandas as pd
import numpy as np
from io import StringIO
import os
from time import time
import seaborn as sns
import hashlib
import re
import string


from datup.io.dataio import (
    download_excel,
    download_csv,
    upload_csv
)

from datup.core.datup import (Datup)

def data_in( self,
    local_path=None,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    datalake=None,
    stage=None,
    filename=None,
    file=None):

    r'''
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log.
        local_path: str,  '/tmp/'  or 'C:\Users\*****' Is necessary write it
            Is the address of the temporal folder of the server which is running the process.
        aws_access_key_id: str, default None
            Is the AWS Access Id provided AWS
        aws_secret_access_key: str, default None
            Is the AWS Access Key provided AWS
        datalake: str, default None
            Is the datalake to use for download the data using the DataIO methods classes
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to download
        filename: str, default None
            Is the name of the filename to download without xlsx or csv suffix
        file:str, default None
            Is the name of the file to download 'excel' or 'csv')


    :rtype: DataFrame
    :return: A DataFrame is return as two-dimensional data structure

    Examples
    --------
    >>> import datup as dt
    >>> dt.data_in( self,local_path=None,aws_access_key_id=None,aws_secret_access_key=None,datalake=None,
        stage=None,filename=None,file=None):
    '''

    try:
        ins = Datup(aws_access_key_id,aws_secret_access_key,datalake,local_path=local_path)

        if (file=='excel'):
            df = download_excel(ins, stage,filename)
        elif (file=='csv'):
            df = download_csv(ins, stage,filename)
        else:
            df = download_csv(ins, stage,filename)

        df1 = pd.concat(df, ignore_index = True)

    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}")
        raise
    except ValueError as error:
        self.logger.exception(f'Exception found: {error}')
    return df1


def data_out(self,df=None,
    local_path=None,
    aws_access_key_id=None,
    aws_secret_access_key=None,
    datalake=None,
    stage=None,
    filename=None):
    r'''
    THIS METHOD HAS BE TESTED

    Parameters
    ----------
        self: Datup
            It is the object type Datup necessary to download using aws credentials and write the log.
        local_path: str,  '/tmp/'  or 'C:\Users\*****' Is necessary write it
            Is the address of the temporal folder of the server which is running the process.
        df: DataFrame
            It is the DataFrame with which want to work
        aws_access_key_id: str, default None
            Is the AWS Access Id provided AWS
        aws_secret_access_key: str, default None
            Is the AWS Access Key provided AWS
        datalake: str, default None
            Is the datalake to use for upload the data using the DataIO methods classes
        stage: str, default None
            It is the set of folders after the datalake to the file that is required to upload
        filename: str, default None
            Is the name of the filename to upload without xlsx or csv suffix,
            the uploaded file is of type 'csv'



    :rtype: DataFrame
    :return: A DataFrame is return as two-dimensional data structure

    Examples
    --------
    >>> import datup as dt
    >>> dt.data_out(self,df=None,local_path=None,aws_access_key_id=None,aws_secret_access_key=None,datalake=None,
        stage=None,filename=None):
    '''
    try:

        ins = Datup(aws_access_key_id,aws_secret_access_key,datalake,local_path=local_path)
        upload_csv(ins,df,stage,filename)

    except FileNotFoundError as error:
        self.logger.exception(f"Exception found: {error}")
        raise
    except ValueError as error:
        self.logger.exception(f'Exception found: {error}')

        return df




class variables_pii:
    try:
        r'''
        THIS METHOD HAS BE TESTED

        This function is used as a complement to the masking and elimination functions

        The class has lists that represent variables of personal identification. Example: general1 and general2

        '''
        general1= ['.documento','^documento','.identificacion','^identificacion','^cedula','^identidad','.identidad','^nacimiento','.nacimiento',
                   '^nombre','.nombre','^sigla','.sigla','.apellido','.email','.telefono','^apellido','^email','^correo','.correo','^telefono',
                   '^direccion','.direccion','^nit','.nit','^codigo','.codigo','^representante',
                   '.representante','^individuo','.individuo','^razon','.razon','^url','.url','^web','.web']
        general2=['.observaciones','^observaciones','.observacion','^observacion','^observ','.observ']

    except variables_pii as error:
        print(error)

def concatenar(df1,df2,id_persona1,id_persona3):
    try:
        '''
        THIS METHOD HAS BE TESTED

        This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
            df1: DataFrame
                It is the DataFrame with which want to work
            df2: DataFrame copy
                It is the DataFrame with which want to work
            id_persona1: tolist
                It is list has the variables of personal identification of the DataFrame
            id_persona3: tolist
                It is list has the personal identification variables concatenated of the DataFrame

        :rtype: DataFrame
        :return: A DataFrame is return as two-dimensional data structure with the personal identification variables concatenated

        Examples
        --------
        >>> import datup as dt
        >>> dt.concatenar(df1,df2,id_persona1,id_persona3)
        '''

        df2=df1.copy()
        ctd=len(id_persona1)
        if (ctd>0):
            inicio=0
            while (inicio<=(ctd-1)):
                if (ctd>=4):
                    if (inicio>=0 and inicio <=3):
                        df2.drop(id_persona1[inicio] ,axis='columns', inplace=True)
                        con=1
                elif (ctd>1 and  ctd <4):
                    if (inicio>=0 and inicio <=1 ):
                        df2.drop(id_persona1[inicio] ,axis='columns', inplace=True)
                        con=2
                else:
                    print('No es posible la concatenacion')
                inicio+=1
        if (con==1):
            df2[id_persona3[0]] = df1[id_persona1[0]]+' '+df1[id_persona1[1]]
            df2[id_persona3[1]] = df1[id_persona1[2]]+' '+df1[id_persona1[3]]
        elif (con==2):
            df2[id_persona3[0]] = df1[id_persona1[0]]+' '+df1[id_persona1[1]]
    except concatenar as error:
        print(error)
    return df2


def concatenar_id (id_persona):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
            id_persona: tolist
                It is list has the variables of personal identification of the DataFrame
            id_persona3: tolist
                It is list has the personal identification variables concatenated of the DataFrame

        :rtype: tolist
        :return: A list is return  with the personal identification variables concatenated
        (Only concatenates the first 4 variables of personal identification)


        Examples
        --------
        >>> import datup as dt
        >>> dt.concatenar_id(id_persona)
        '''
        id_persona1=id_persona.copy()
        id_persona2=[]
        id_persona3=[]
        con=0
        ctd=len(id_persona1)
        if (ctd>0):
            inicio=0
            while (inicio<=(ctd-1)):
                if (ctd>=4):
                    if (inicio>=0 and inicio <=2):
                        id_persona2.append(id_persona1[inicio]+'-'+id_persona1[inicio+1])
                        con=1
                elif (ctd>1 and  ctd <4):
                    if (inicio==0 ):
                        id_persona2.append(id_persona1[inicio]+'-'+id_persona1[inicio+1])
                        con=2
                else:
                    print('No es posible la concatenacion')
                    id_persona3=id_persona1
                inicio+=1
        else:
            print('No hay variables de identificacion personal')

        if (con==1):
            id_persona2.pop(1)
            id_persona1.pop(0)
            id_persona1.pop(0)
            id_persona1.pop(0)
            id_persona1.pop(0)
            id_persona3=id_persona2+id_persona1
        elif (con==2):
            id_persona1.pop(0)
            id_persona1.pop(0)
            id_persona3=id_persona2+id_persona1
    except concatenar_id as error:
        print(error)
    return (id_persona3)

def organizar(df2,id_persona1):
    r'''
    THIS METHOD HAS BE TESTED

    --->>> This function is used as a complement to the masking and elimination functions

    Parameters
    ----------
        df2: DataFrame
            It is the DataFrame with which want to work
        id_persona: tolist
            It is list has the variables of personal identification of the DataFrame

    :rtype: DataFrame
    :return: A DataFrame is return as two-dimensional data structure with the personal identification variables concatenated
    in the original position of the variables
    (Only concatenates the first 4 variables of personal identification)


    Examples
    --------
    >>> import datup as dt
    >>> dt.organizar(df2,id_persona1)
    '''
    ctd1=len(id_persona1)
    ctd=len(df2.columns)
    b=df2.columns.tolist()
    a=0
    c=0
    order=[]
    d=0
    if (ctd1 >4):
        while a<=(ctd-1):
            if(b[a]==id_persona1[4]):
                c=a
            a+=1
        while d<=(ctd-1):
            if(d==c):
                order.append(ctd-2)
                order.append(ctd-1)
            order.append(d)
            d+=1

        order.pop(ctd)
        order.pop(ctd)

        df2 = df2[df2.columns[order]]

    elif (ctd1 ==4):
        while a<=(ctd-1):
            if(b[a]==0):
                c=a
            a+=1
        while d<=(ctd-1):
            if(d==c):
                order.append(ctd-2)
                order.append(ctd-1)
            order.append(d)
            d+=1

        order.pop(ctd)
        order.pop(ctd)

        df2 = df2[df2.columns[order]]

    elif (ctd1 >=2 and ctd1 <=3):
        while a<=(ctd-1):
            if(b[a]==0):
                c=a
            a+=1
        while d<=(ctd-1):
            if(d==c):
                order.append(ctd-1)
            order.append(d)
            d+=1

        order.pop(ctd)
        df2 = df2[df2.columns[order]]


    return df2


def profiling(df):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        --->>> This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
            df: DataFrame
                It is the DataFrame with which want to work
        :rtype: information
        :return: Returns specified information from the dataframe: Description, number of columns, NaN, dtype


        Examples
        --------
        >>> import datup as dt
        >>> dt.profiling(df)
        '''
        df.info()
        df.isnull().sum()
        df.describe()
    except profiling as error:
        print(error)

def normalize(s):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        --->>> This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
            s: str
                Word of dtype string
        :rtype: String
        :return: Returns a string without accents


        Examples
        --------
        >>> import datup as dt
        >>> dt.normalize(s)
        '''
        replacements = (
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
         )
        for a, b in replacements:
             s = s.replace(a, b).replace(a.upper(), b.upper())
    except normalize as error:
        print(error)
    return s

def observaciones (df1):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        --->>> This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
        df: DataFrame
            It is the DataFrame with which want to work
        :rtype: String
        :return: Returns a string with word Observaciones or string with void values


        Examples
        --------
        >>> import datup as dt
        >>> dt.observaciones (df1)
        '''
        columnas=df1.columns
        ctd_columnas=len(columnas)
        individuo1=variables_pii()
        id_=list()
        inicio=0
        while (inicio <= (ctd_columnas-1)) :
            for inter in individuo1.general2:
                if (re.findall(inter,normalize(columnas[inicio].lower()))):
                        id_=columnas[inicio]
            inicio+=1
    except observaciones as error:
        print(error)

    return (id_)

def organizar_observaciones (df1):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        --->>> This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
        df1: DataFrame
            It is the DataFrame with which want to work
        :rtype: String
        :return: Returns a dataframe with a change of order. The last and penultimate column are exchanged.

        (The last column corresponds to the 'Puntajes' of the dataframe, and the penultimate corresponds to the 'Observaciones' field)


        Examples
        --------
        >>> import datup as dt
        >>> dt.organizar_observaciones (df1)
        '''

        ctd=len(df1.columns)
        b=df1.columns
        order=[]
        d=0
        while d<=(ctd-1):
            order.append(d)
            if (d==ctd-1):
                order.append(ctd-2)
            d+=1
        order.pop(ctd-2)
        df1 = df1[df1.columns[order]]
    except organizar_observaciones as error:
        print(error)
    return df1


def eliminar_duplicados(id_persona):
    try:
        r'''
        THIS METHOD HAS BE TESTED

        --->>> This function is used as a complement to the masking and elimination functions

        Parameters
        ----------
        id_persona: list
            It is list has the variables of personal identification of the DataFrame
        :rtype: list
        :return: Returns a list without duplicate values


        Examples
        --------
        >>> import datup as dt
        >>> dt.eliminar_duplicados(id_persona)
        '''

        id_persona1=list()

        for a in id_persona:
            if a not in id_persona1:
                id_persona1.append(a)

    except eliminar_duplicados as error:
        print(error)

    return id_persona1
