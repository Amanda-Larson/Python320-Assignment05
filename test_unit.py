from unittest import TestCase
from unittest.mock import Mock, patch
from loguru import logger
from pymongo import MongoClient
import pysnooper
import unittest
import users
import user_status


class TestMongoDBConnection(TestCase):
    """MongoDB Connection"""
    def runTest(self):
        assert True
    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        TestCase.__init__(self)
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def load_tables(self):
        self.mongo = TestMongoDBConnection()
        with self.mongo:
            # mongodb database; it all starts here
            db = self.mongo.connection.media

            # collection in database
            TestUserAccounts = db["TestUserAccounts"]
            TestStatusAccounts = db["TestStatusAccounts"]

            # Create default user
            user_id = 'ldconejo79'
            user_name = 'Luis'
            user_last_name = 'Conejo'
            user_email = 'luisconejo@conejo.com'
            self.assertEqual(TestUserAccounts.add_user(user_id, user_email, user_name, user_last_name), True)

            # Create default status
            user_id = 'ldconejo79'
            status_id = 'ldconejo79_001'
            status_text = 'My first status'
            self.assertEqual(TestStatusAccounts.add_status(user_id, status_id, status_text), True)

    def test_add_user(self):
        self.mongo = TestMongoDBConnection()
        with self.mongo:
            # mongodb database; it all starts here
            db = self.mongo.connection.media

            # collection in database
            TestUserAccounts = db["TestUserAccounts"]

            user_id = 'ldconejo80'
            user_name = 'Luis'
            user_last_name = 'Conejo'
            user_email = 'luisconejo@conejo.com'
            self.assertEqual(TestUserAccounts.add_user(user_id, user_email, user_name, user_last_name), True)

    def test_add_user_duplicated(self):
        self.mongo = TestMongoDBConnection()
        with self.mongo:
            # mongodb database; it all starts here
            db = self.mongo.connection.media

            # collection in database
            TestUserAccounts = db["TestUserAccounts"]

            user_id = 'ldconejo79'
            user_name = 'Luis'
            user_last_name = 'Conejo'
            user_email = 'luisconejo@conejo.com'
            self.assertEqual(TestUserAccounts.add_user(user_id, user_email, user_name, user_last_name), False)

    def test_modify_user(self):
        self.mongo = TestMongoDBConnection()
        with self.mongo:
            # mongodb database; it all starts here
            db = self.mongo.connection.media

            # collection in database
            TestUserAccounts = db["TestUserAccounts"]
            user_id = 'ldconejo79'
            user_name = 'Elisa'
            user_last_name = 'Cornejo'
            user_email = 'elisa.conejo@conejo.com'
            self.assertEqual(TestUserAccounts.modify_user(user_id, user_email, user_name, user_last_name), True)

    def test_modify_user_not_found(self):
        user_id = 'ldconejo80'
        user_name = 'Elisa'
        user_last_name = 'Cornejo'
        user_email = 'elisa.conejo@conejo.com'
        self.assertEqual(self.user_collection.modify_user(user_id, user_email, user_name, user_last_name), False)

    def test_search_user(self):
        user_id = 'ldconejo79'
        user_name = 'Luis'
        user_last_name = 'Conejo'
        user_email = 'luisconejo@conejo.com'
        result = self.user_collection.search_user(user_id)
        self.assertEqual(result.user_id, user_id)
        self.assertEqual(result.user_name, user_name)
        self.assertEqual(result.user_last_name, user_last_name)
        self.assertEqual(result.user_email, user_email)

    def test_search_user_not_found(self):
        user_id = 'ldconejo80'
        result = self.user_collection.search_user(user_id)
        self.assertEqual(result, None)

    def test_delete_user(self):
        user_id = 'ldconejo79'
        self.assertEqual(self.user_collection.delete_user(user_id), True)

    def test_delete_user_not_found(self):
        user_id = 'joemissing'
        self.assertEqual(self.user_collection.delete_user(user_id), False)

    def test_add_status(self):
        # Needs a user for new status
        user_id = 'ldconejo79'
        status_id = 'ldconejo79_000'
        status_text = 'My first status'
        self.assertEqual(self.status_collection.add_status(user_id, status_id, status_text), True)

    def test_add_duplicated(self):
        # Needs a user for new status
        user_id = 'ldconejo79'
        status_id = 'ldconejo79_001'
        status_text = 'My first status'
        self.assertEqual(self.status_collection.add_status(user_id, status_id, status_text), False)

    def test_modify_status(self):
        user_id = 'ldconejo79'
        status_id = 'ldconejo79_001'
        status_text = 'Excited to be on this social network'
        self.assertEqual(self.status_collection.modify_status(status_id, user_id, status_text), True)

    def test_modify_status_not_found(self):
        user_id = 'ldconejo80'
        status_id = 'ldconejo80_001'
        status_text = 'Excited to be on this social network'
        self.assertEqual(self.status_collection.modify_status(status_id, user_id, status_text), False)

    def test_search_status(self):
        status_id = 'ldconejo79_001'
        status_text = 'My first status'
        result = self.status_collection.search_status(status_id)
        self.assertEqual(result.status_id, status_id)
        self.assertEqual(result.status_text, status_text)

    def test_search_status_not_found(self):
        status_id = 'ldconejo80_001'
        result = self.status_collection.search_status(status_id)
        self.assertEqual(result, None)

    def test_delete_status(self):
        status_id = 'ldconejo79_001'
        self.assertEqual(self.status_collection.delete_status(status_id), True)

    def test_delete_status_not_found(self):
        status_id = 'joemissing_001'
        self.assertEqual(self.status_collection.delete_status(status_id), False)

    # def tearDown(self):
    #     self.database.drop_tables([
    #         UsersTable,
    #         StatusTable
    #     ])
    #     self.database.close()


# if __name__ == "__main__":
#     unittest.main()
if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMongoDBConnection)
    unittest.TextTestRunner().run(suite)
