async def check_gamename(client, gamename) -> bool:
    found = client.find_one()