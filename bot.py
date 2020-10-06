import os
import asyncio
from utils.robot import Robot
from discord.ext import commands


# Load environment variables if they aren't loaded yet
if not os.getenv("DISCORD_TOKEN"):
	from dotenv import load_dotenv
	load_dotenv()

prefixes = ["?", "x?", "d?"]

client = Robot(
	command_prefix=commands.when_mentioned_or(*prefixes),
	case_insensitive=True,
	owner_id=os.getenv("OWNER_ID")
)
print(os.getenv("OWNER_ID"))

# Load dem extentions
extensions = [
    "cogs.mod",
	"cogs."
]

for cog in extensions:
    try:
        print(f"Loading cog: {cog}")
        client.load_extension(cog)
    except Exception as e:
        print(f"Error while loading cog: {cog}")

client.run(os.getenv("DISCORD_TOKEN"))
