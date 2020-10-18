from discord.ext import commands

import statcord


class StatcordPost(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.key = self.bot.config.statcord_token
		self.api = statcord.Client(self.bot,self.key)
		if not self.bot.dev:
			self.api.start_loop()


	@commands.Cog.listener()
	async def on_command(self,ctx):
		self.api.command_run(ctx)


def setup(bot):
	bot.add_cog(StatcordPost(bot))