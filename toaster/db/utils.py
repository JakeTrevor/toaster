from typing import List, Tuple
from discord import Message
from sqlalchemy.orm import Session as session_type


from db.engine import Session
from db.models import Game


def add_game(game: Message) -> None:
    new_game = Game(game)
    with Session() as session:
        session.merge(new_game)
        session.commit()


def winrate(player1: str, player2: str, group: str) -> Tuple[int, int]:
    """returns [games_won, games_played]"""
    session: session_type
    with Session() as session:
        games: List[Game] = session.query(Game).filter(
            Game.group == group,
            Game.game_string.contains(player1),
            Game.game_string.contains(player2)
        ).all()

    # eliminate case where players are on the same team
    games = [game for game in games if game.are_opposing(player1, player2)]

    games_played = len(games)
    games_won = len(
        [game for game in games if game.is_winner(player1, player2)])

    return (games_won, games_played)


def print_games():
    with Session() as session:
        games: List[Game] = session.query(Game).all()
        for game in games:
            print(game.game_string)
