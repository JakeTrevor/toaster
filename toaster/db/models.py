from discord import Message, TextChannel, Guild  # type imports
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

from utils import clean_team


Base = declarative_base()


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)  # eq to message.id
    date = Column(DateTime, nullable=False)
    group = Column(String, nullable=False)
    game_string = Column(String, nullable=False)
    winning_team = Column(String, nullable=False)
    losing_team = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"< Game {self.game_string} >"

    def __contains__(self, player: str) -> bool:
        return player in self.game_string

    def __init__(self, game: Message) -> None:
        self.id = game.id
        self.date = game.created_at

        channel: TextChannel = game.channel
        guild: Guild = channel.guild
        # ! not sure if this is best
        self.group = guild.name + "///" + channel.name

        self.game_string: str = game.content
        if ">" in self.game_string:
            teams = self.game_string.split(">")
            self.winning_team = clean_team(teams[0])
            self.losing_team = clean_team(teams[1])
        else:
            teams = self.game_string.split("<")
            self.winning_team = clean_team(teams[1])
            self.losing_team = clean_team(teams[0])

    def are_opposing(self, player1: str, player2: str) -> bool:
        if not player2:
            return True

        return (
            (player1 in self.winning_team and player2 in self.losing_team) or
            (player1 in self.losing_team and player2 in self.winning_team)
        )

    def is_winner(self, player1: str, player2: str) -> bool:
        return True
