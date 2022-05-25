"""
Classes for user information for the social network project
"""
# pylint: disable=R0903
# pylint: disable=C0103
# pylint: disable=E0401

import csv
from loguru import logger
from pymongo import MongoClient
from pymongo import ReturnDocument
from pymongo import ASCENDING
# from user_status import *


logger.info("Let's get to debugging users.py")
logger.add("users_and_status.log", backtrace=True, diagnose=True)


class UserMongoDBConnection:
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

    @staticmethod
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
        mongo = UserMongoDBConnection()
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
                    UserAccounts.create_index([('USER_ID', ASCENDING)], unique=True)
                    return result
            except FileNotFoundError:
                print('File not found')
                return False

    @staticmethod
    def add_user(user_id, email, user_name, user_last_name):
        """
        Adds a new user to the collection
        """
        mongo = UserMongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]

            new_user = {"USER_ID": user_id}

            if UserAccounts.count_documents({'USER_ID': user_id}) > 0:
                logger.info("Reject new user  -  user_id already exists")
                print('This user already exists, try again.')
                return False
            new_user = {"USER_ID": user_id, "EMAIL": email,
                        "NAME": user_name, "LASTNAME": user_last_name}
            UserAccounts.insert_one(new_user)
            return True

    @staticmethod
    def modify_user(user_id, email, user_name, user_last_name):
        """
        Modifies an existing user
        """
        mongo = UserMongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            if UserAccounts.count_documents({'USER_ID': user_id}) < 1:
                logger.info("This user does not exist, please try again.")
                return False
            query = {'USER_ID': user_id}
            updated = {"$set": {"USER_ID": user_id, "EMAIL": email,
                                "NAME": user_name, "LASTNAME": user_last_name}}
            UserAccounts.update_one(query, updated)
            print(f'User {user_id} has been successfully updated.')
            return ReturnDocument

    @staticmethod
    def delete_user(user_id):
        """
        Deletes an existing user
        """
        mongo = UserMongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            StatusUpdates = db["StatusUpdates"]
            try:
                query = {'USER_ID': user_id}
                UserAccounts.delete_one(query)
                StatusUpdates.delete_many(query)
                logger.info(f'User ID {user_id}, deleted.')
                return True
            except Exception as error:
                print('An error has occurred - user was not deleted.')
                logger.info(error)
                return False

    @staticmethod
    def search_user(user_id):
        """
        Searches for user data
        """
        mongo = UserMongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            UserAccounts = db["UserAccounts"]
            found = UserAccounts.find_one({"USER_ID": user_id})
            return found
