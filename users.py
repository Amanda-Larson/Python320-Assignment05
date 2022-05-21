"""
Classes for user information for the social network project
"""
# pylint: disable=R0903

from loguru import logger
from pymongo import MongoClient
from pymongo import ReturnDocument
from pymongo import errors as e
import pymongoshell
import csv
import pysnooper

logger.info("Let's get to debugging users.py")
logger.add("users_and_status.log", backtrace=True, diagnose=True)


class MongoDBConnection:
    """MongoDB Connection"""

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


class UserCollection:
    """
    Contains a collection of Users objects
    """

    def load_users(filename):
        """
        Opens a CSV file with user data and
        adds it to an existing instance of
        UserCollection

        Requirements:
        - If a user_id already exists, it
        will ignore it and continue to the
        next.
        - Returns False if there are any errors
        (such as empty fields in the source CSV file)
        - Otherwise, it returns True.
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]

            # tried to figure out a quicker way to connect to database,
            # but it closes the connection before anything can happen

            # with UserCollection.connect_to_db() as UserAccounts:

            try:
                with open(filename, newline='', encoding="UTF-8") as file:
                    file_users = csv.DictReader(file)
                    result = UserAccounts.insert_many(file_users)
                    # UserAccounts.createIndex({'USER_ID':1}, {unique:true})
            except FileNotFoundError:
                print('File not found')
                return False

    @staticmethod
    def add_user(user_id, email, user_name, user_last_name):
        """
        Adds a new user to the collection
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            if user_id in UserAccounts.find():
                logger.info("Reject new user  -  user_id already exists")
                return False
            new_user = {"USER_ID": user_id, "EMAIL": email, "NAME": user_name, "LASTNAME": user_last_name}
            UserAccounts.insert_one(new_user)
            return True

    @staticmethod
    @pysnooper.snoop
    def modify_user(user_id, email, user_name, user_last_name):
        """
        Modifies an existing user
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            # if user_id not in UserAccounts["USER_ID"]:
            # logger.info(f'{user_id} not in the database')
            # return False
            UserAccounts.find_one_and_update({"USER_ID": user_id}, {"USER_ID": user_id, "EMAIL": email,
                                                                    "NAME": user_name, "LASTNAME": user_last_name},
                                             return_document=ReturnDocument.AFTER)
            return ReturnDocument

    @staticmethod
    def delete_user(user_id):
        """
        Deletes an existing user
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            if user_id not in self.database:
                logger.info(f'{user_id} not in the database')
                return False
            del self.database[user_id]
            return True

    def search_user(user_id):
        """
        Searches for user data
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            found = UserAccounts.find_one({"USER_ID": user_id})
            return found
