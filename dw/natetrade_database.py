
__author__ = "Nathan Ward"

import logging
from sys import stdout
from os import environ
from time import time
import mysql.connector
from mysql.connector import Error

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)

#Local logging to stdout.
#Comment this out if using in production with a built-in logger.
handler = logging.StreamHandler(stdout)
_LOGGER.addHandler(handler)


class SQLError(Exception):
    """Exception class if there is a problem talking to the SQL DB."""
    pass


class StrictSchemaError(Exception):
    """Exception class if data passed does match the schema."""
    pass


class DatabaseHelper(object):
    def __init__(self):
        self.sql_user = environ['SQL_USERNAME']
        self.sql_pw = environ['SQL_PASSWORD']
        self.sql_endpoint = environ['SQL_HOSTNAME']
        self.sql_dbname = 'db'
    
    def generic_select_query(self, query_string: str) -> list:
        """
        Function to execute a select query. Returns a list of dicts.
        """
        try:
            cnx = mysql.connector.connect(
                user = self.sql_user,
                password = self.sql_pw,
                host = self.sql_endpoint,
                database = self.sql_dbname
            )
        except Error as e:
            _LOGGER.exception('Problem accessing natetrade SQL database. {0}'.format(e))
            raise SQLError('Problem accessing natetrade SQL database. {0}'.format(e))
        
        try:
            if cnx.is_connected():
                cursor = cnx.cursor(dictionary=True)
                
                start_time = time()
                
                cursor.execute(query_string)
                result = cursor.fetchall()
                
                end_time = time()
                execution_time = round((end_time - start_time), 3)
                
                _LOGGER.info('Returned {0} rows of data in {1} seconds.'.format(len(result), execution_time))
                
                return result
        except Error as e:
            _LOGGER.exception('Problem getting greek data. {0}'.format(e))
            raise SQLError('Problem getting greek data. {0}'.format(e))
        finally:
            if cnx.is_connected():
                cursor.close()
                cnx.close()
    
    def contract_price_over_time(self, ticker: str, option_type: str, expiration: str, strike: int) -> list:
        """
        Example query to get the last 1000 trades over a contract.
        
        Could be used for instance to track changes in implied volatility or greeks.
        """
        if option_type not in 'pc':
            raise StrictSchemaError('Invalid arguments. {0}'.format(locals()))
        
        query = """
        SELECT *
        FROM db.greeks
        WHERE ticker = '{sym}'
        AND option_type = '{op_type}'
        AND expiration = '{exp}'
        AND strike = {strike}
        ORDER BY timestamp
        DESC
        LIMIT 1000;
        """.format(
            sym = ticker,
            op_type = option_type,
            exp = expiration,
            strike = strike
        )
        
        return self.generic_select_query(query)
    
    def top_stocks_activity(self, date: str) -> list:
        """
        Example query to get the top 50 stocks by transactions.
        """
        query = """
        SELECT *
        FROM db.daily_underlying 
        WHERE date = '{date}'
        ORDER BY num_transactions 
        DESC
        LIMIT 50
        """.format(date = date)
        
        return self.generic_select_query(query)

