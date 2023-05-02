from Logs import logevents
import asyncio
import json
from Connection import client
from config import __add_path

asyncio.run(__add_path)


# Methods that belong to this class
# __get_user_count              Done        ErrHandling: Done
# __create_user                 Done        ErrHandling: Not Required
# __add_user                    Done        ErrHandling: Done
# __update_user                 Done        ErrHandling: Done
# __delete_user                 Done        ErrHandling: Done
# __add_alt                     Done        ErrHandling: Done
# __change_default              Done        ErrHandling: Done
# __verify_user                 Done        ErrHandling: Done
# __remove_verification         Done        ErrHandling: Done
# __ban_user                    Done        ErrHandling: Done
# __unban_user                  Done        ErrHandling: Done


# Data to be fed into this class is to be validated before hand
# as no error handeling has been done for invalid data
class User():
    def __init__(self):
        # Setting up the logger class for logging errors
        self.logger = logevents()

        # Setting up the collection to be used
        self.database = 'UserData'
        self.collection = 'User'
        self.client = client[self.database][self.collection]

        # Creating a default user object
        self.userid = None
        self.discord_username = None
        self.discord_userid = None
        self.game_usernames = []
        self.default_username = None
        self.stats = []
        self.verified = False
        self.banned = False

    # Method to get the total count of successfully registerd users
    async def __get_user_count(self):
        try:
            return int(self.client.count_documents({}))
        except Exception as error:
            errorid = await self.logger.log_error(class_name='User', function_name='__get_user_count', message=error)
            print(
                f"An error occoured in the User class within the __get_user_count function, check error logs with id {errorid} for more details")


# Create User
    # Create a template for adding a new user and sends the query with the templated data as a return

    async def __create_user(self, discord_username: str, discord_userid: int, game_username):
        # Filling in the data
        self.userid = self.__get_user_count() + 1
        self.discord_username = discord_username
        self.discord_userid = discord_userid
        self.default_username = game_username
        self.game_usernames.append(game_username)

        # Creating the query to be send in connection
        query = {
            'userid': self.userid,
            'discord_username': self.discord_username,
            'discord_userid': self.discord_userid,
            'game_usernames': self.game_usernames,
            'default_username': self.default_username,
            'verified': self.verified,
            'stats': self.stats,
            'banned': self.banned
        }

        # Convert to query to a string and send
        return query

# Add User
    async def __add_user(self, discord_username: str, discord_userid: int, game_username):
        query = await self.__create_user(discord_username, discord_userid, game_username)

        # Add the user to the database
        try:
            self.client.insert_one(query)
            print("New user Added Successfully")
            return
        except Exception as error:

            errorid = await self.logger.log_error(class_name='User', function_name='__add_user', message=error)
            print(
                f"An error occoured in the User class within the __add_user function, check error logs with id {errorid} for more details")

# Update user
    async def __update_user(self, discord_userid: int, to_update: str, update_to) -> bool:
        try:
            # Find the user document using the userid
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            # Make the requested update
            user[to_update] = update_to

            # Push the updated document to the database
            self.client.replace_one(query, user)

            print(
                f'Updated {to_update} for {user["discord_username"]} to {update_to}')
            return True

        except Exception as error:
            errorid = self.logger.log_error(
                class_name='User', function_name='__update_user', message=error)
            print(
                f'An error occoured in the User class within the __update_user function, check error logs with id {errorid} for more details')
            return False

# Delte User
    async def __delete_user(self, discord_userid: int) -> bool:
        try:
            query = {'discord_userid': discord_userid}
            self.client.delete_one(query)
            print('Deleted the user successfully')
            return True
        
        except Exception as error:
            errorid = self.logger.log_error(
                class_name='User', function_name='__delete_user', message=error)
            print(
                f'An error occoured in the User class within the __delete_user function, check error logs with id {errorid} for more details')
            return False

# Adding Alt account
    async def __add_alt(self, discord_userid: int, alt_username: str) -> bool:
        try:
            # Get the user from the database
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            # Update the user document locally
            user['gameusernames'].append(alt_username)

            # Push the changed object to the database
            self.client.replace_one(query, user)
            print("Alt account added successfully")
            return True
        
        except Exception as error:
            errorid = self.logger.log_error(class_name='User', function_name='__add_alt', message=error)
            print(f'An error occoured in the Uer class wtihin the __add_alt function, check error logs with id {errorid} for more details')
            return False

# Change Default
    async def __change_default(self, discord_userid: int, game_username: str) -> bool:
        try:
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            if game_username in user['game_usernames']:
                user['default_username'] = game_username
            else:
                raise Exception('This username dosent belong to the author')
        
            self.client.replace_one(query, user)
            print("Default accoutn changed successfully")
            return True
        
        except Exception as error:
            errorid = self.logger.log_error(class_name='User', function_name='__change_default', message=error)
            print(f'An error occoured in the Uer class wtihin the __change_default function, check error logs with id {errorid} for more details')
            return False

# Verify User
    async def __verify_user(self, discord_userid: int) -> bool:
        try:
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            if user['verified']:
                raise Exception("User is already verified, Use the __remove_verification to change user verification")
            else:
                user['verified'] = True
            
            self.client.replace_one(query, user)
            print("User Verified successfully")
            return True

        except Exception as error:
            errorid = self.logger.log_error(class_name='User', function_name='__verify_user', message=error)
            print(f'An error occoured in the Uer class wtihin the __verify_user function, check error logs with id {errorid} for more details')
            return False
        
# Remove Verification
    async def __remove_verification(self, discord_userid: int) -> bool:
        try:
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            if user['verified']:
                user['verified'] = False
            else:
                raise Exception("User is Not verified")
            
            self.client.replace_one(query, user)
            print("User UnVerified successfully")
            return True

        except Exception as error:
            errorid = self.logger.log_error(class_name='User', function_name='__remove_verification', message=error)
            print(f'An error occoured in the Uer class wtihin the __remove_verification function, check error logs with id {errorid} for more details')
            return False

# Ban User
    async def __ban_user(self, discord_userid: int) -> bool:
        try:
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            if user['banned']:
                raise Exception("User is already banned")
            else:
                user['banned'] = True
            
            self.client.replace_one(query, user)
            print("User Banned successfully")
            return True

        except Exception as error:
            errorid = self.logger.log_error(class_name='User', function_name='__ban_user', message=error)
            print(f'An error occoured in the Uer class wtihin the __ban_user function, check error logs with id {errorid} for more details')
            return False

# Unban User
    async def __unban_user(self, discord_userid: int) -> bool:
        try:
            query = {'discord_userid': discord_userid}
            user = self.client.find_one(query)

            if user['banned']:
                user['banned'] = False
            else:
                raise Exception("User is not currently banned")
            
            self.client.replace_one(query, user)
            print("User Unbanned successfully")
            return True

        except Exception as error:
            errorid = self.logger.log_error(class_name='User', function_name='__unban_user', message=error)
            print(f'An error occoured in the Uer class wtihin the __unban_user function, check error logs with id {errorid} for more details')
            return False

        



if __name__ == '__main__':
    obj = User()
    asyncio.run(obj._User__get_user_count())