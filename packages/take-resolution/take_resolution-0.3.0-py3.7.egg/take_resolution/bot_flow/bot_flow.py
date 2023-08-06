__author__ = 'Moises Mendes and Gabriel Salgado'
__version__ = '0.3.0'
__all__ = [
    'build_dataframe',
    'select_bot',
    'select_flow',
    'query'
]

import pandas as pd
import pyspark as ps


DF = pd.DataFrame
SDF = ps.sql.DataFrame
CONTEXT = ps.SQLContext


def build_dataframe(sql_context: CONTEXT, database: str, table: str) -> SDF:
    """Build Pyspark DataFrame from Spark SQL context.
    
    :param sql_context: Pyspark SQL context to connect to database and table.
    :type sql_context: ``pyspark.SQLContext``
    :param database: Database name.
    :type database: ``str``
    :param table: Table name.
    :type table: ``str``
    :return: Pyspark DataFrame pointing to specified table.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return sql_context.table(f'{database}.{table}')


def select_bot(df: SDF, bot_column: str, bot_identity: str, app_column: str, app_value: str) -> SDF:
    """Select element on table by bot.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param bot_column: Column that indicates the bot identity.
    :type bot_column: ``str``
    :param bot_identity: Bot identity.
    :type bot_identity: ``str``
    :param app_column: Column that indicates application.
    :type app_column: ``str``
    :param app_value: Value on application flow_column.
    :type app_value: ``str``
    :return: Filtered spark dataframe by bot.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.filter((df[bot_column] == bot_identity) & (df[app_column] == app_value))


def select_flow(df: SDF, flow_column: str) -> SDF:
    """Select bot flow column on spark dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :param flow_column: Column that indicates the bot flow.
    :type flow_column: ``str``
    :return: Spark dataframe with only bot flow.
    :rtype: ``pyspark.sql.DataFrame``
    """
    return df.select(flow_column)


def query(df: SDF) -> DF:
    """Query spark dataframe getting pandas dataframe.
    
    :param df: Spark dataframe.
    :type df: ``pyspark.sql.DataFrame``
    :return: Pandas dataframe with the data.
    :rtype: ``pandas.DataFrame``
    """
    return df.toPandas()
