import os
import asyncio
import sys
import discord
from utils import usefull
from main import robot
from discord.ext import commands
from jishaku.help_command import DefaultEmbedPaginatorHelp


# Load config
config = usefull.load("config.json")

# Configure intents
intents = discord.Intents.default()
# Set priviliged intents based off of config
intents.members = config.intents.members
intents.presences = config.intents.presences

dev = False
# was a command line arg passed?
# yes this is a bad way to do this. Too bad
if (len(sys.argv) > 1):
	dev = True

prefixes = config.prefixes
if dev:
	prefixes = config.dev_prefixes

client = robot.Robot(
	command_prefix=commands.when_mentioned_or(*prefixes),
	case_insensitive=True,
	owner_ids=config.owners,
	intents=intents
)

# Load dem extentions
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")
# jishaku is special
client.load_extension("jishaku")

token = config.token
if client.dev:
	token = config.dev_token

client.run(token)
