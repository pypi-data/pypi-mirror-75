import pandas as pd
import sqlalchemy
import pymysql
import pymssql
from sqlalchemy.types import Integer, Text, String, DateTime

class DatabasesIO:
    def __init__(
        self,
        conn_name,
        db_user,
        db_pass,
        db_name
    ):
        self.conn_name = conn_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def download_mssql(
        self,
        cls,
        table_name
    ):
        """
        Return a DataFrame with the information into the database's table
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: DatabasesIO
                It is the object type DatabasesIO
            cls: Datup
                Is the datup object necessary for saving into logger 
            table_name: str
                Is the name of the table to extract the information

        :return: Return a DataFrame
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> datup = dt.Datup()
        >>> db=dt.DatabasesIO(conn_name,db_user,db_pass,db_name)
        >>> db.download_mssql(datup,'table_name')        
        """
        try:
            driver_name = "mssql+pymssql"
            port = "1433"
            engine=sqlalchemy.create_engine(f"{driver_name}://{self.db_user}:{self.db_pass}@{self.conn_name}:{port}/{self.db_name}")
            df = pd.DataFrame(pd.read_sql_table(table_name, engine))
        except IOError as error:
            cls.logger.exception(f"Exception found: {error}")
        return df

    def download_mysql(
        self,
        cls,
        table_name
    ):
        """
        Return a DataFrame with the information into the database's table
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: DatabasesIO
                It is the object type DatabasesIO
            cls: Datup
                Is the datup object necessary for saving into logger 
            table_name: str
                Is the name of the table to extract the information

        :return: Return a DataFrame
        :rtype: DataFrame

        Examples
        --------
        >>> import datup as dt
        >>> datup = dt.Datup()
        >>> db=dt.DatabasesIO(conn_name,db_user,db_pass,db_name)
        >>> db.download_mysql(datup,'table_name')  
        """
        try:
            driver_name = "mysql+pymysql"
            engine=sqlalchemy.create_engine(f"{driver_name}://{self.db_user}:{self.db_pass}@{self.conn_name}/{self.db_name}")
            df = pd.DataFrame(pd.read_sql_table(table_name, engine))
        except IOError as error:
            cls.logger.exception(f"Exception found: {error}")
        return df

    def upload_mysql(
        self,
        cls,
        df,
        table_name,
        if_exists="replace",
        index=False
    ):
        """
        Does not return any information, the method save the DataFrame information into a table in the 
        database previously filled
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: DatabasesIO
                It is the object type DatabasesIO
            cls: Datup
                Is the datup object necessary for saving into logger 
            df: DataFrame
                It is the DataFrame with which want to work
            table_name: str
                Is the name of the table to save the information
            if_exists: str, default 'replace'
                How to behave if the table already exists. Options available are:
                    *   fail: Raise a ValueError.
                    *   replace: Drop the table before inserting new values.
                    *   append: Insert new values to the existing table.
            index: Bool, default False
                If true, write DataFrame index as a column. Uses index_label as the column name in the table.

        Examples
        --------
        >>> import datup as dt
        >>> datup = dt.Datup()
        >>> db=dt.DatabasesIO(conn_name,db_user,db_pass,db_name)
        >>> db.upload_mysql(datup,df,'table_name')  
        """
        try:
            driver_name = "mysql+pymysql"
            engine=sqlalchemy.create_engine(f"{driver_name}://{self.db_user}:{self.db_pass}@{self.conn_name}/{self.db_name}")
            df.to_sql(table_name,engine,if_exists=if_exists,index=index)
        except IOError as error:
            cls.logger.exception(f"Exception found: {error}")

    def upload_mssql(
        self,
        cls,
        df,
        table_name,
        if_exists="replace",
        index=False
    ):
        """
        Does not return any information, the method save the DataFrame information into a table in the 
        database previously filled
        
        THIS METHOD HAS BE TESTED

        Parameters
        ----------
            self: DatabasesIO
                It is the object type DatabasesIO
            cls: Datup
                Is the datup object necessary for saving into logger 
            df: DataFrame
                It is the DataFrame with which want to work
            table_name: str
                Is the name of the table to save the information
            if_exists: str, default 'replace'
                How to behave if the table already exists. Options available are:
                    *   fail: Raise a ValueError.
                    *   replace: Drop the table before inserting new values.
                    *   append: Insert new values to the existing table.
            index: Bool, default False
                If true, write DataFrame index as a column. Uses index_label as the column name in the table.

        Examples
        --------
        >>> import datup as dt
        >>> datup = dt.Datup()
        >>> db=dt.DatabasesIO(conn_name,db_user,db_pass,db_name)
        >>> db.upload_mssql(datup,df,'table_name')  
        """
        try:
            driver_name = "mssql+pymssql"
            port = "1433"
            engine=sqlalchemy.create_engine(f"{driver_name}://{self.db_user}:{self.db_pass}@{self.conn_name}:{port}/{self.db_name}")
            df.to_sql(table_name,engine,if_exists=if_exists,index=index)
        except IOError as error:
            cls.logger.exception(f"Exception found: {error}")