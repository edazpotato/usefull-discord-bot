import os
import asyncio
from utils import robot, usefull
from discord.ext import commands


# Load config
config = usefull.load("config.json")

# Configure intents
intents = discord.Intents.default()
# Set priviliged intents based off of config
intents.members = config.intents.members
intents.presences = config.intents.presences

client = robot.Robot(
	command_prefix=commands.when_mentioned_or(*config.prefixes),
	case_insensitive=True,
	owner_id=config.owners,
	intents=intents
)

# Load dem extentions
for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(config.token)
