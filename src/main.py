import os
import asyncio
import discord
from discord.ext import commands

from utils.env_loader import get_env

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=">", intents=intents)

TOKEN = get_env("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("The DISCORD_TOKEN environment variable is not set.")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    # Sync application (slash) commands. For faster development use a
    # `DEV_GUILD` environment variable with your guild ID to sync there
    # instantly. Otherwise this attempts a global sync (which can take
    # up to an hour to propagate).
    try:
        dev_guild = get_env("DEV_GUILD")
        if dev_guild:
            guild_obj = discord.Object(id=int(dev_guild))
            await bot.tree.sync(guild=guild_obj)
            print(f"Synced commands to guild {dev_guild}")
        else:
            synced = await bot.tree.sync()
            print(f"Globally synced {len(synced)} commands")
    except Exception as e:
        print("Command sync failed:", e)


async def load_extensions():
    commands_dir = os.path.join(os.path.dirname(__file__), "commands")
    # Determine package name robustly. When run as a package (`python -m src.main`)
    # `__package__` will be the package name (e.g. 'src'). If the module is run
    # as a script, fall back to the commands directory's parent name.
    package = __package__ or os.path.basename(os.path.dirname(__file__))

    for file in os.listdir(commands_dir):
        if file.endswith(".py") and not file.startswith("__"):
            ext = f"{package}.commands.{file[:-3]}"
            await bot.load_extension(ext)
            print(f"Loaded extension: {ext}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
