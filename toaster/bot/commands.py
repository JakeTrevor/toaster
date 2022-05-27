from typing import List
from discord import Message, TextChannel
from db.utils import add_game

from config import COMMAND
from utils import OPPOSITION, get_games, is_game, is_winner


async def undefined(*args):
    print("unrecognised command")


async def winrate(command: Message, player1: str = "", player2: str = "", *args) -> None:
    if not player1:
        await command.channel.send(
            "Please provide a player to calculate the winrate for")
        return

    if player2.lower() == "everyone":
        player2 = ""

    games = await get_games(command.channel.history(limit=None), player1, player2)
    games: List[str] = [game.content for game in games]
    player2 = player2 or "everyone"

    games_played = len(games)
    if games_played == 0:
        await command.channel.send(f"{player1} hasn't played any games against {player2}")
        return

    games_won = 0
    [games_won := games_won + 1 for each in games if is_winner(player1, each)]

    await command.channel.send(
        f"__**{player1}'s winrate against {player2}:**__\n {games_won} / {games_played} games won \n winrate of {games_won/games_played*100}%")
    ...


async def getTeams(message: Message, *args) -> None:
    print("concocting teams")


async def generateCache(message: Message, *args) -> None:
    channel: TextChannel = message.channel

    game: Message
    count = 0
    async for game in channel.history(limit=None):
        if is_game(game.content):
            count += 1
            add_game(game)
    await channel.send(f"cache generated, {count} games found")


async def getHelp(message: Message, *args) -> None:
    text = f"""
    __**Commands:**__
    __{COMMAND}winrate <player1> [player2]__
        - prints the winrate of player 1 against player 2
        - if a second player is not provided, calculates winrate against everyone
    
    __{COMMAND}generateCache__
        - reads through entire chat history to find all previous games
        - this is an expensive operation, and should only be done occasionaly (once) for setup

    __{COMMAND}getTeams__
    """

    channel: TextChannel = message.channel
    await channel.send(text)
    return

commands = {
    "winrate": winrate,
    "getteams": getTeams,
    "generatecache": generateCache,
    "help": getHelp,
}
