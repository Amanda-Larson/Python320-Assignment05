"""
classes to manage the user status messages
"""
# pylint: disable=R0903
from loguru import logger
import csv
from pymongo import ReturnDocument
from pymongo import MongoClient

logger.info("Let's get to debugging user_status/py")
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


class UserStatusCollection:
    """
    Collection of UserStatus messages
    """

    @staticmethod
    def load_status_updates(filename):
        """
        Opens a CSV file with status data and adds it to an existing
        instance of UserStatusCollection

        Requirements:
        - If a status_id already exists, it will ignore it and continue to
          the next.
        - Returns False if there are any errors(such as empty fields in the
          source CSV file)
        - Otherwise, it returns True.
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            StatusUpdates = db["StatusUpdates"]

            try:
                with open(filename, newline='', encoding="UTF-8") as file:
                    file_users = csv.DictReader(file)
                    result = StatusUpdates.insert_many(file_users)
                    # StatusUpdates.createIndex({'USER_ID': 1}, unique=True)
                    return result

            except FileNotFoundError:
                print('File not found')

    @staticmethod
    def add_status(status_id, user_id, status_text):
        """
        add a new status message to the collection
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            StatusUpdates = db["StatusUpdates"]
            UserAccounts = db["UserAccounts"]

            if StatusUpdates.count_documents({'STATUS_ID': status_id}) > 0 and UserAccounts.count_documents({'USER_ID': user_id}) > 0:
                logger.info("Reject new status  -  status_id already exists")
                print('This status already exists, try again.')
                return False
            new_status = {"STATUS_ID": status_id, "USER_ID": user_id, "STATUS_TEXT": status_text}
            StatusUpdates.insert_one(new_status)
            return True

    @staticmethod
    def modify_status(status_id, user_id, status_text):
        """
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            StatusUpdates = db["StatusUpdates"]
            if StatusUpdates.count_documents({'USER_ID': user_id}) < 1:
                logger.info("This user does not exist, please try again.")
                return False
            query = {'USER_ID': user_id}
            updated = {"$set": {"STATUS_ID": status_id, "USER_ID": user_id, "STATUS_TEXT": status_text}}
            StatusUpdates.update_one(query, updated)
            print(f'User {user_id}\'s status has been successfully updated.')
            return ReturnDocument

    @staticmethod
    def delete_status(status_id):
        """
        deletes the status message with id, status_id
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media

            # collection in database
            StatusUpdates = db["StatusUpdates"]
            try:
                query = {'USER_ID': status_id}
                StatusUpdates.delete_one(query)
                logger.info(f'Status ID {status_id} has been deleted.')
                return True
            except Exception as error:
                print('An error has occurred - status has not been deleted.')
                logger.info(error)
                return False

    @staticmethod
    def search_status(status_id):
        """
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        """
        mongo = MongoDBConnection()
        with mongo:
            # mongodb database; it all starts here
            db = mongo.connection.media
            try:
                # collection in database
                StatusUpdates = db["StatusUpdates"]
                found = StatusUpdates.find_one({"STATUS_ID": status_id})
                return found
            except Exception as error:
                logger.info(error)
