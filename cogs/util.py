import typing
import urllib
import discord
from dateutil import parser
from discord.ext import commands
from utils import permissions

class Util(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="invite", aliases=["inv"])
	async def invite_command(self, ctx):
		perms_int = 2147483639#2146958847
		await ctx.send(f"<https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions={perms_int}>")

	#@commands.command(name="help", aliases=["sendhelp", "commands"], usage="[command | catagory]")
	async def help_command(self, ctx, *, command: typing.Optional[str]=None):
		pass

def setup(bot):
	bot.add_cog(Util(bot))