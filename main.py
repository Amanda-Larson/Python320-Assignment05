"""
# Title: main driver for a simple social network project
# Who: ALarson
# What/When: 4/24/2022 - started assignment
"""
import csv


import user_status
from users import UserCollection as uc
from user_status import UserStatusCollection as us
import pysnooper


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


def print_mdb_collection(collection_name):
    """for each collection/table pring the document/row"""
    for doc in collection_name.find():
        print(doc)


# @pysnooper.snoop
# def init_user_accounts():
#     """
#     Creates and returns a new instance of UserCollection
#     """
#     mongo = MongoDBConnection()
#     with mongo:
#         # mongodb database; it all starts here
#         db = mongo.connection.media
#
#         # collection in database
#         UserAccounts = db["UserAccounts"]
#         return UserAccounts


def init_status_collection():
    """
    Creates and returns a new instance of UserStatusCollection
    """
    mongo = MongoDBConnection()
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.media

        # collection in database
        StatusUpdates = db["StatusUpdates"]
        return StatusUpdates


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
        UserAccounts = db["StatusUpdates"]

        try:
            with open(filename, newline='', encoding="UTF-8") as file:
                file_users = csv.DictReader(file)
                result = UserAccounts.insert_many(file_users)
                return result
        except FileNotFoundError:
            print('File not found')
            return False


def save_users(filename, user_collection):
    """
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such as an invalid filename).
    - Otherwise, it returns True.
    """
    header = ['USER_ID', 'EMAIL', 'NAME', 'LASTNAME']
    try:
        with open(filename, mode='a', newline='', encoding="UTF-8") as file:
            writer = csv.DictWriter(file, delimiter=',', fieldnames=header)
            writer.writeheader()
            for key, values in user_collection().database:
                row = {key: values}
                writer.writerow(row)
                return True
    except FileNotFoundError:
        print(f'File {filename} not found')
        return False


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
                return result

        except FileNotFoundError:
            print('File not found')


def save_status_updates(filename, status_collection):
    """
    Saves all statuses in status_collection into a CSV file

    Requirements:
    - If there is an existing file, it will overwrite it.
    - Returns False if there are any errors(such an invalid filename).
    - Otherwise, it returns True.
    """

# @pysnooper.snoop(depth=3)
def add_user(user_id, email, user_name, user_last_name):
    """
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """
    new_user = uc.add_user(user_id, email, user_name, user_last_name)
    return new_user


def update_user(user_id, email, user_name, user_last_name):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there are any errors.
    - Otherwise, it returns True.
    """
    updated_user = uc.modify_user(user_id, email, user_name, user_last_name)
    return updated_user


def delete_user(user_id):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    del_user = uc.delete_user(user_id)
    return del_user


def search_user(user_id):
    """
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    """
    find_user = uc.search_user(user_id)
    return find_user


def add_status(status_id, user_id, status_text):
    """
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    add_new_status = us.add_status(status_id, user_id, status_text)
    return add_new_status


def update_status(status_id, user_id, status_text):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    updated_status = us.modify_status(status_id, user_id, status_text)
    return updated_status


def delete_status(status_id):
    """
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    del_status = us.delete_status(status_id)
    return del_status


def search_status(status_id):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    find_status = us.search_status(status_id)
    return find_status
