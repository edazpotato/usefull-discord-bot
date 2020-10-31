import sys
import traceback
import discord
from discord.ext import commands, tasks
from utils import usefull, permissions

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
			await ctx.error(ctx.strings.ERR_COMMAND_ON_COOLDOWN.format(err))
		elif (isinstance(err, commands.MemberNotFound)):
			await ctx.error(ctx.strings.ERR_COMMAND_MEMBER_NOT_FOUND.format(err))
		elif (isinstance(err, permissions.AuthorLacksPermssions)):
			await ctx.error(ctx.strings.ERR_COMMAND_AUTHOR_LACKS_PERMS.format(err))
		elif (isinstance(err, permissions.BotLacksPermssions)):
			await ctx.error(ctx.strings.ERR_COMMAND_BOT_LACKS_PERMS.format(err))
		elif (isinstance(err, commands.UserNotFound)):
			await ctx.error(ctx.strings.ERR_USER_NOT_FOUND.format(err))
		elif (isinstance(err, commands.NotOwner)):
			await ctx.error(ctx.strings.ERR_NOT_OWNER.format(err))
		elif (isinstance(err, discord.NotFound)):
			await ctx.error(ctx.strings.ERR_FORBIDDEN.format(err))
		elif (isinstance(err, discord.Forbidden)):
			await ctx.error(ctx.strings.ERR_FORBIDDEN.format(err))
		else:
			if (self.bot.dev):
				tracebackString = "".join(traceback.format_exception(type(err), err, err.__traceback__))
				await ctx.warning(f"Ignoring exception in command {ctx.command}:")
				await ctx.send(f"```py\n{tracebackString}\n```")
			else:
				await ctx.error(ctx.strings.ERR)
				print(f"{c.FAIL}Ignoring exception in command {ctx.command}{c.END}:", file=sys.stderr)
				traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(Events(bot))
