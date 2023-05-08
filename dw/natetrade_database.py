
__author__ = "Nathan Ward"

import logging
from sys import stdout
from os import environ
import mysql.connector
from mysql.connector import Error
from utilities import APIKeys

_LOGGER = logging.getLogger()
_LOGGER.setLevel(logging.INFO)

#Local logging to stdout.
#Comment this out if using in production with a built-in logger.
handler = logging.StreamHandler(stdout)
_LOGGER.addHandler(handler)


class DatabaseHelper(object):
    def __init__(self):
        self.sql_user = environ['SQL_USERNAME']
        self.sql_pw = environ['SQL_PASSWORD']
        self.sql_endpoint = environ['SQL_HOSTNAME']
        self.sql_dbname = 'db'
        self.sql_dbport = 3306
    
    