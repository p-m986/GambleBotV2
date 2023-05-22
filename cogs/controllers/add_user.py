async def add_user(client, userdata):
    client.insert_one(userdata)