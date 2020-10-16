import discord
from discord.ext import commands, tasks

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.event()
	async def on_command_error(self, ctx, err):
		if (isinstance(err, commands.CommandNotFound)):
			return
		if (isinstance(err, commands.CommandOnCooldown)):
			return await ctx.send(f"This command has a {err.rate} second coolddown.\nPlease wait {err.retry_after} seconds then try again.")
		return await ctx.send(f"An unknown error occured when executing that command.\nThis issue has been noted and will be fixed as soon as possible.")


def setup(bot):
    bot.add_cog(Events(bot))
