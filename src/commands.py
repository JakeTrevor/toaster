import re
import discord
from typing import AsyncIterator, List

OPPOSITION = r" ?(<|>) ?"
CONTENSTANT = r"[, ]*"


async def undefined(*args):
    print("unrecognised command")


def is_game(game: str) -> bool:
    if "@" in game:
        return False
    if not ("<" in game or ">" in game):
        return False

    return bool(re.match(
        r"^(\w+[, ]*)+(<|>) *(\w+[, ]*)+$",
        game
    ))


def winner(player: str, game: str) -> bool:
    teams = re.split(OPPOSITION, game)
    if ">" in game:
        winning_team = teams[0]
    else:
        winning_team = teams[2]
    return player in winning_team


async def get_games(player1: str, player2: str, messages: AsyncIterator) -> List[str]:
    games = []
    async for message in messages:
        text = message.content
        if is_game(text) and (player1 in text) and (player2 in text):
            games.append(text)
    return games


async def winrate(command: discord.Message, *args) -> None:
    if len(args) == 0:
        await command.channel.send(
            "Please provide a player to calculate the winrate for")
        return

    player1 = args[0]
    player2 = args[1] if 1 < len(args) else ""
    games = await get_games(player1, player2, command.channel.history(limit=None))
    player2 = player2 or "everyone"

    games_played = len(games)
    if games_played == 0:
        await command.channel.send(f"{player1} hasn't played any games against {player2}")
        return

    games_won = 0
    [games_won := games_won + 1 for each in games if winner(player1, each)]

    await command.channel.send(
        f"__**{player1}'s winrate against {player2}:**__\n {games_won} / {games_played} games won \n winrate of {games_won/games_played*100}%")
    ...


async def getteams(message, *args):
    print("concocting teams")


commands = {
    "winrate": winrate,
    "getteams": getteams,
}
