import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
load_dotenv()

print("test")

#bot = discord.Client(intents=discord.Intents.all())
bot = commands.bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('lancement du bot')
    # Sync des commandes
    try:
        #sync
        total_command_sync = await bot.tree.sync()
        print(f'nombre de commandes synchronisées: {len(total_command_sync)}')
    except Exception as e:
        #throw erreur
        print(e)


@bot.event
async def on_message(message: discord.Message):
    # empecher le bot de s'auto appeler
    if message.author.bot:
        return
    
    if message.content.lower() == 'bonjour':
        channel = message.channel
        await channel.send("Bonjour!")

        author = message.author
        await author.send("Bonjour!")


    if message.content.lower() == "bonjour":
        channel_id = os.getenv('CHANNEL_ID')
        await channel_id.send("Bonjour!")


@bot.tree.command(name='test', description='commande test')
async def test(interaction: discord.Integration):
    await interaction.response.send_message("Ceci est une commande test")

bot.run(os.getenv('DISCORD_TOKEN'))