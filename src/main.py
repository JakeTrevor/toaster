import discord
from decouple import config
from commands import commands, undefined


client = discord.Client()


@client.event
async def on_redy():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    text: str = message.content

    if text.startswith(config("COMMAND")):
        text = text[1:].split(" ")

        command = text[0].lower()
        args = text[1:]

        await commands.get(command, undefined)(message, *args)

    ...

client.run(config("TOKEN"))
