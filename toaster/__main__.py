import click
from db.admin import setup_database

from bot.main import main
from db.utils import print_games


@click.group()
def toaster():
    pass


@toaster.command("setupDB", help="Create required database tables; loads config from env")
def setup():
    setup_database()


@toaster.command("run", help="Run the toaster bot")
def run():
    main()
    pass


@toaster.command("test")
def test():
    print_games()


if __name__ == "__main__":
    toaster()
