"""
Provides a basic frontend
"""
import sys
from loguru import logger
import pysnooper
import main
from users import UserCollection as uc

logger.info("Let's get to debugging")
logger.add("out.log", backtrace=True, diagnose=True)


# @pysnooper.snoop(depth=3)
def load_users():
    """
    Loads user accounts from a file
    """
    filename = input('Enter filename of user file: ')
    uc.load_users(filename)


def load_status_updates():
    """
    Loads status updates from a file
    """
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename)


# @pysnooper.snoop()
def add_user():
    """
    Adds a new user into the database
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if not main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name):
        print("An error occurred while trying to add new user")
    else:
        print("User was successfully added")


def update_user():
    """
    Updates information for an existing user
    """
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    update = main.update_user(user_id, email, user_name, user_last_name)
    return update

# @pysnooper.snoop
def search_user():
    """
    Searches a user in the database
    """
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id)
    if not result:
        print("ERROR: User does not exist")
    else:
        print(f"User ID: {result['USER_ID']}")
        print(f"Email: {result['EMAIL']}")
        print(f"Name: {result['NAME']}")
        print(f"Last name: {result['LASTNAME']}")


# @pysnooper.snoop()
def delete_user():
    """
    Deletes user from the database
    """
    user_id = input('User ID: ')
    if not main.delete_user(user_id):
        print("An error occurred while trying to delete user")
    else:
        print("User was successfully deleted")


# @pysnooper.snoop()
def save_users():
    """
    Saves user database into a file
    """
    filename = input('Enter filename for users file: ')
    main.save_users(filename)


# @pysnooper.snoop()
def add_status():
    """
    Adds a new status into the database
    """
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.add_status(status_id, user_id, status_text):
        print("An error occurred while trying to add new status")
    else:
        print("New status was successfully added")


# @pysnooper.snoop()
def update_status():
    """
    Updates information for an existing status
    """
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if not main.update_status(status_id, user_id, status_text):
        print("An error occurred while trying to update status")
    else:
        print("Status was successfully updated")


# @pysnooper.snoop(depth=3)
def search_status():
    """
    Searches a status in the database
    """
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id)
    if not result.status_id:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")


# @pysnooper.snoop(depth=3)
def delete_status():
    """
    Deletes status from the database
    """
    status_id = input('Status ID: ')
    if not main.delete_status(status_id):
        print("An error occurred while trying to delete status")
    else:
        print("Status was successfully deleted")


def save_status():
    """
    Saves status database into a file
    """
    filename = input('Enter filename for status file: ')
    main.save_status_updates(filename)


def quit_program():
    """
    Quits program
    """
    sys.exit()


if __name__ == '__main__':
    # UserAccounts = main.init_user_accounts()
    # StatusUpdates = main.init_status_collection()
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': save_status,
        'Q': quit_program
    }

    while True:
        # main.init_user_accounts(main.UserAccounts)
        # main.init_status_collection()
        user_selection = input("""
                            A: Load user database
                            B: Load status database
                            C: Add user
                            D: Update user
                            E: Search user
                            F: Delete user
                            G: Save user database to file
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            L: Save status database to file
                            Q: Quit

                            Please enter your choice: """)
        if user_selection.upper() in menu_options:
            menu_options[user_selection.upper()]()
        else:
            print("Invalid option")
