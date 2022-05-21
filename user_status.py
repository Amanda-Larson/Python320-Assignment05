"""
classes to manage the user status messages
"""
# pylint: disable=R0903
from loguru import logger

logger.info("Let's get to debugging user_status/py")
logger.add("users_and_status.log", backtrace=True, diagnose=True)

#
# class UserStatus:
#     """
#     class to hold status message data
#     """
#
#     def __init__(self, status_id, user_id, status_text):
#         self.status_id = status_id
#         self.user_id = user_id
#         self.status_text = status_text
#         logger.info("Object instantiated")


class UserStatusCollection:
    """
    Collection of UserStatus messages
    """

    # def __init__(self):
    #     self.database = {}
    #     logger.info("Set up the status database.")

    def add_status(status_id, user_id, status_text):
        """
        add a new status message to the collection
        """
        if status_id in self.database:
            logger.info("Rejects new status if status_id already exists")
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        self.database[status_id] = new_status
        return True

    def modify_status(self, status_id, user_id, status_text):
        """
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        """
        if status_id not in self.database:
            logger.info("Status_id does not exist")
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        return True

    def delete_status(self, status_id):
        """
        deletes the status message with id, status_id
        """
        if status_id not in self.database:
            logger.info("Failed - status does not exist")
            return False
        del self.database[status_id]
        return True

    def search_status(self, status_id):
        """
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        """
        if status_id not in self.database:
            logger.info("Failed - status does not exist")
            return UserStatus(None, None, None)
            # return False
        return self.database[status_id]
