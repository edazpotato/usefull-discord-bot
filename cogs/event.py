import sys
import traceback
import discord
from discord.ext import commands, tasks
from utils import usefull

c = usefull.colors

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# This uses lots of code from here: https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):

		# this stops this from handling commands that have their own specififc error handlers
		if hasattr(ctx.command, 'on_error'):
			return

		# Errors to ignore
		ignored = (commands.CommandNotFound, commands.TooManyArguments)

		# Get original error
		err = getattr(err, 'original', err)

		# Ignore ignored errors
		if isinstance(err, ignored):
			return

		# User feedback via reactions
		await ctx.message.add_reaction(self.bot.emoji.no)

		# H A N D L E R S
		if (isinstance(err, commands.MissingRequiredArgument)):
			await ctx.error(ctx.strings.ERR_COMMAND_MISSING_REQ_PARAM.format(err))
		elif (isinstance(err, commands.ArgumentParsingError)):
			await ctx.error(ctx.strings.ERR_COMMAND_ARG_PARSE.format(err))
		elif (isinstance(err, commands.PrivateMessageOnly)):
			await ctx.error(ctx.strings.ERR_COMMAND_DM_ONLY.format(err))
		elif (isinstance(err, commands.NoPrivateMessage)):
			await ctx.error(ctx.strings.ERR_COMMAND_NO_DM.format(err))
		elif (isinstance(err, commands.DisabledCommand)):
			await ctx.error(ctx.strings.ERR_COMMAND_DISABLED.format(err))
		elif (isinstance(err, commands.CommandOnCooldown)):
			await ctx.error(ctx.strings.ERR_COMMAND_RATELIMIT.format(err))
		else:
			print(f'{c.FAIL}Ignoring exception in command {ctx.command}{c.END}:', file=sys.stderr)
			traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(Events(bot))
