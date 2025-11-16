import os
import asyncio
import discord
from discord.ext import commands

from utils.env_loader import get_env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = get_env("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("The DISCORD_TOKEN environment variable is not set.")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


async def load_extensions():
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    for file in os.listdir(commands_dir):
        if file.endswith(".py") and not file.startswith("__"):
            ext = f"bot.commands.{file[:-3]}"
            await bot.load_extension(ext)
            print(f"Loaded extension: {ext}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
