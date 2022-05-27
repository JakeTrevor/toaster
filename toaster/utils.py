from discord import Message
import re
from typing import AsyncIterator, List

OPPOSITION = r" ?(<|>) ?"
CONTENSTANT = r"[, ]*"


def is_game(game: str) -> bool:
    if "@" in game:
        return False
    if not ("<" in game or ">" in game):
        return False

    return bool(re.match(
        r"^(\w+[, ]*)+(<|>) *(\w+[, ]*)+$",
        game
    ))


def is_winner(player1: str, player2: str, game: str) -> bool:
    teams = re.split(OPPOSITION, game)
    if ">" in game:
        winning_team = teams[0]
    else:
        winning_team = teams[2]
    return player1 in winning_team


def clean_team(team: str) -> str:
    return ", ".join(
        [each for each in re.split(",| ", team) if each]
    )


async def get_games(messages: AsyncIterator, player1: str = None, player2: str = "") -> List[Message]:
    if player1 == None:
        is_ok = is_game
    else:
        def is_ok(x: str):
            return is_game(x) and (
                player1 in x) and (
                player2 in x)

    games = []
    async for message in messages:
        text = message.content
        if is_ok(text):
            games.append(message)
    return games
