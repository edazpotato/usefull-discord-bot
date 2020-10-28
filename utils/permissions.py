import discord
import os
import traceback
import sys
from discord.ext import commands
from utils import usefull

# Based off of https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/permissions.py

owners = [os.getenv("OWNER_ID")]

c = usefull.colors

def is_owner(ctx):
	return ctx.author.id in owners

# Custom errors
class AuthorLacksPermssions(commands.CheckFailure):
	"""Raised when the author of a command does not have sufficent permissions to execute it"""
	def __init__(self, missing_perms, *args):
		self.missing_perms = missing_perms
		missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in missing_perms]
		if len(missing) > 2:
			fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
		else:
			fmt = ' and '.join(missing)
		message = 'Author requires {} permission(s) to run this command.'.format(fmt)
		super().__init__(message, *args)
class BotLacksPermssions(commands.CheckFailure):
	"""Raised when the bot does not have sufficent permissions to execute the command"""
	def __init__(self, missing_perms, *args):
		self.missing_perms = missing_perms
		missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in missing_perms]
		if len(missing) > 2:
			fmt = '{}, and {}'.format(", ".join(missing[:-1]), missing[-1])
		else:
			fmt = ' and '.join(missing)
		message = 'Bot requires {} permission(s) to run this command.'.format(fmt)
		super().__init__(message, *args)

# author checks
async def check_author_permissions(ctx, perms, *, check=all):
	if ctx.author.id in owners:
		return True

	resolved = ctx.channel.permissions_for(ctx.author)
	return check(getattr(resolved, name, None) == value for name, value in perms.items())

# decorator
def author_has_permissions(*, check=all, **perms):
	async def pred(ctx):
		if (not await check_author_permissions(ctx, perms, check=check)):
			raise AuthorLacksPermssions(perms)
		return True

	return commands.check(pred)

# Bot checks
async def check_bot_permissions(ctx, perms, *, check=all):
	resolved = ctx.channel.permissions_for(ctx.me)
	return check(getattr(resolved, name, None) == value for name, value in perms.items())

# decorator
def bot_has_permissions(*, check=all, **perms):
	async def pred(ctx):
		if (not await check_bot_permissions(ctx, perms, check=check)):
			raise BotLacksPermssions(perms)
		return True

	return commands.check(pred)


async def check_priv(ctx, member):
	try:
		# Self checks
		if member == ctx.author:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_SELF.format(ctx))
			return True
		if member.id == ctx.bot.user.id:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT.format(ctx))
			return True

		# Check if the bot can do stuff
		if ctx.guild.me.top_role == member.top_role:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT_EQUAL.format(ctx))
			return True
		if ctx.guild.me.top_role < member.top_role:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT_HIGHER.format(ctx))
			return True

		# Now permission check
		if member.id in owners:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT_OWNER.format(ctx))
			return True

		# Check if user bypasses
		if ctx.author.id == ctx.guild.owner_id:
			return False
		if ctx.author.id in owners:
			return False

		if member.id == ctx.guild.owner.id:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_GUILD_OWNER.format(ctx))
			return True
		if ctx.author.top_role == member.top_role:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_AUTHOR_EQUAL.format(ctx))
			return True
		if ctx.author.top_role < member.top_role:
			await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_AUTHOR_HIGHER.format(ctx))
			return True
		return False
	except Exception as err:
		if (ctx.bot.dev):
			tracebackString = "".join(traceback.format_exception(type(err), err, err.__traceback__))
			await ctx.warning(f"Ignoring exception in command {ctx.command}:")
			await ctx.send(f"```py\n{tracebackString}\n```")
		else:
			print(f"{c.FAIL}Error checking privilages:{c.END} {err}")
			traceback.print_exception(type(err), err, err.__traceback__, file=sys.stderr)


def can_send(ctx):
	return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).send_messages


def can_embed(ctx):
	return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).embed_links


def can_upload(ctx):
	return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).attach_files


def can_react(ctx):
	return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).add_reactions


def is_nsfw(ctx):
	return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.is_nsfw()
