from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
load_dotenv()
from Logs import logevents

class database():
    def __init__(self):
        self.uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWORD')}@data.rg5fs5b.mongodb.net/?retryWrites=true&w=majority"
        self.has_connected = False
        self.client = None
    
    async def get_client(self):
        if not self.client:
            self.client = await self.__connect()
        return self.client
    
    async def __connect(self):
        client = MongoClient(self.uri, server_api = ServerApi('1'))
        await self.__test_connection(client= client)
        self.client = client
        return self.client

    async def __test_connection(self, client):
        try:
            client.admin.command('ping')
            self.has_connected = True   
            print("Successfully connected to the database")
        except Exception as error:
            obj = logevents()
            await obj.log_error(class_name='database', function_name='__test_connection', message=error)
            print(f"An error occoured in the database class within the __test_connection function, check error logs with id {obj.errorid}")
        return