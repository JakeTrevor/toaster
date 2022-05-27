from discord import Client, Message
from bot.commands import commands, undefined

from config import TOKEN, COMMAND

client = Client()


def handle_new_game():
    pass


@client.event
async def on_redy():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: Message):
    if message.author == client.user:
        return

    text: str = message.content.lower()

    if text.startswith(COMMAND):
        text = text[1:].split(" ")

        command = text[0]
        args = text[1:]

        await commands.get(command, undefined)(message, *args)
    elif "<" in text or ">" in text:
        handle_new_game()
    ...


def main():
    client.run(TOKEN)


if __name__ == "__main__":
    main()
