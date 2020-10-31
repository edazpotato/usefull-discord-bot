import typing
import urllib
import discord
from dateutil import parser
from discord.ext import commands
from utils import permissions

class Admintools(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.check(commands.is_owner())
	@commands.command(name="say", aliases=["echo", "print"], usage="<text to say>")
	async def say_command(self, ctx, *, msg: str):
		try:
			await ctx.message.delete()
		except:
			pass
		await ctx.send(msg)

def setup(bot):
	bot.add_cog(Admintools(bot))