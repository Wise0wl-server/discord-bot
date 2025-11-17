import discord
import os
from dotenv import load_dotenv
import logging
from discord.ext import commands

# documentation: https://discordpy.readthedocs.io/en/latest/api.html#discord.Intents

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="wise0wl_bot.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()


# intents.auto_moderation                 = True
# intents.auto_moderation_configuration   = True
# intents.auto_moderation_execution       = True
# intents.bans                            = True
# intents.dm_messages                     = True
# intents.dm_polls                        = True
# intents.dm_reactions                    = True
# intents.dm_typing                       = True
# intents.emojis                          = True
# intents.emojis_and_stickers             = True
# intents.expressions                     = True
# intents.guild_messages                  = True
# intents.guild_polls                     = True
# intents.guild_reactions                 = True
# intents.guild_scheduled_events          = True
# intents.guild_typing                    = True
# intents.guilds                          = True
# intents.integrations                    = True
# intents.invites                         = True
intents.members                         = True
intents.message_content                 = True
# intents.messages                        = True
# intents.moderation                      = True
# intents.polls                           = True
# intents.presences                       = True
# intents.reactions                       = True
# intents.typing                          = True
# intents.value                           = True
# intents.voice_states                    = True
# intents.webhooks                        = True





bot = commands.Bot(command_prefix="!", intents=intents)







############################################################################
################################            ################################
################################   EVENTS   ################################
################################            ################################
############################################################################


@bot.event
async def on_ready():
    print("lancement du bot")

@bot.event
# permet de vérifier l'arrivée de nouveaux membres et de les mentionner
async def on_member_join(member):
    await member.send(f"Bienvenue {member.name}")


@bot.event
async def on_message(message):
    # ne pas s'auto check
    if message.author == bot.user:
        return

    # permet de supprimer un message ciblé + mention
    if "test" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} message enlevé")

    # permet de continuer de process
    await bot.process_commands(message)










##############################################################################
################################              ################################
################################   COMMANDS   ################################
################################              ################################
##############################################################################

# !hello -> renvoie le bonjour avec mention au user 
@bot.command()
async def hello(ctx):
    await ctx.send(f"Bonjour {ctx.author.mention}!")


# !assign_default_role -> permet d'ajouter le role par defaut (nom du role 'Wise0wl_noAuth')
@bot.command()
async def assign_default_role(ctx):
    role_nouvel_arrivant = "Wise0wl_noAuth"
    role = discord.utils.get(ctx.guild.roles, name=role_nouvel_arrivant)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} possède maintenant le role {role_nouvel_arrivant}")
    else:
        await ctx.send(f"Le role {role_nouvel_arrivant} n'existe pas.")


# !remove_default_role -> permet d'enlever le role par defaut (nom du role 'Wise0wl_noAuth')
@bot.command()
async def remove_default_role(ctx):
    default_role = "Wise0wl_noAuth"
    role = discord.utils.get(ctx.guild.roles, name=default_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} ne possède plus le role {default_role}")
    else:
        await ctx.send(f"Le role {default_role} n'existe pas.")


# !check_role -> permet de recevoir un message si on a le role.
mention_role = "Wise0wl_noAuth"
@bot.command()
@commands.has_role(mention_role)
async def check_role(ctx):
    await ctx.send(f"Vous recevez ce message puisque vous avez le role {mention_role}")

@check_role.error
async def check_role_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        await ctx.send(f"{ctx.author.mention} Une erreur est survenue, veuillez reessayer plus tard.")









#################################################################################
################################                 ################################
################################   DM et REPLY   ################################
################################                 ################################
#################################################################################

# !DM {msg} -> retourne en MP {msg} à l'utilisateur
@bot.command()
async def DM(ctx, *, msg):
    await ctx.author.send(f"{msg}")


# !dm -> si l'utilisateur dis "bonjour" apres la commande, alors il recevra en MP bonjour {user} de la part du bot
@bot.command()
async def dm(ctx, *, msg):
    if msg == "":
        return
    
    if msg == "bonjour":
        await ctx.author.send(f"Bonjour {ctx.author.name}")
    else:
        await ctx.author.send(f"jsp frr")

# !reply -> retourne une reponse en mentionnant la personne
@bot.command()
async def reply(ctx):
    await ctx.reply(f"Bonjour {ctx.author.mention}.")







#############################################################################################
################################                             ################################
################################   POLL & EMBED & REACTIONS  ################################
################################                             ################################
#############################################################################################

# !poll {question} -> crée un poll et ajoute des emojies comme reponse
@bot.command()
async def poll(ctx, *, question):
    embed = discord.Embed(title="New poll", description=question)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍") # windows + .  => accede a la librairie d'emojis
    await poll_message.add_reaction("👎")

#envoie une erreur au besoin si les arguments ne sont pas bon, si il y a un probleme avec la commande ou autre.
@poll.error
async def check_role_error(ctx, error):
    await ctx.send(f"{ctx.author.mention} Une erreur est survenue, veuillez reessayer plus tard.")
    embed = discord.Embed(title="Erreur", description=error)
    await ctx.send(embed=embed)

        















bot.run(token, log_handler=handler, log_level=logging.DEBUG)