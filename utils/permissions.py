"""
This is based off of a great permissions thing by AlexFlipnote.
You can find the original here: https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/default.py
"""

import discord
import os

from discord.ext import commands

owners = [os.getenv("OWNER_ID")]


def is_owner(ctx):
	return ctx.author.id in owners


async def check_permissions(ctx, perms, *, check=all):
	if ctx.author.id in owners:
		return True

	resolved = ctx.channel.permissions_for(ctx.author)
	return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
	async def pred(ctx):
		return await check_permissions(ctx, perms, check=check)
	return commands.check(pred)


async def check_priv(ctx, member):
	try:
		# Self checks
		if member == ctx.author:
			return await ctx.send(f"Thou shalt not {ctx.command.name} thyself!")
		if member.id == ctx.bot.user.id:
			return await ctx.send("Dont bully me pls")

		# Check if bot owner
		if member.id in owners:
			return await ctx.send(f"You found an {ctx.command.name}able user! Good for you.")
		if ctx.author.id in owners:
			return False

		# Check if user is guild owner
		if ctx.author.id == ctx.guild.owner.id:
			return False

		# Now permission check
		if member.id == ctx.guild.owner.id:
			return await ctx.send(f"I'm sorry, but I can't let you {ctx.command.name} the ***owner***.")
		if ctx.author.top_role == member.top_role:
			return await ctx.send(f"Sorry, but you and that person have the same perms, so you can't {ctx.command.name} them.")
		if ctx.author.top_role < member.top_role:
			return await ctx.send(f"DO NOT CHALLENGE AUTHORITY, *{ctx.author.name}*!")
	except Exception:
		pass


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