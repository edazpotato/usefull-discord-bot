"""
This is based off of a great permissions thing by AlexFlipnote.
You can find the original here: https://github.com/AlexFlipnote/discord_bot.py/blob/master/utils/permissions.py
"""

import discord
import os

from discord.ext import commands

owners = [os.getenv("OWNER_ID")]


def is_owner(ctx):
    return ctx.author.id in owners

# Custom errors
class AuthorLacksPermssions(commands.CheckFailure):
    """Raised when the author of a command does not have sufficent permissions to execute it"""
    pass
class BotLacksPermssions(commands.CheckFailure):
    """Raised when the bot does not have sufficent permissions to execute the command"""
    pass

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
            raise AuthorLacksPermssions(perms=perms)
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
            raise BotLacksPermssions(perms=perms)
        return True

    return commands.check(pred)


async def check_priv(ctx, member):
    try:
        # Self checks
        if member == ctx.author:
            return await ctx.error(f"Sorry, but you can't {ctx.command.name} yourself.")
        if member.id == ctx.bot.user.id:
            return await ctx.error("No u")

        # Check if the bot can do stuff
        if ctx.guild.me == member.top_role:
            return await ctx.error(f"Sorry, but {ctx.command.name} doesn't work on someone who is equal in power to me.")
        if ctx.guild.me < member.top_role:
            return await ctx.error(f"Sorry, but {ctx.command.name} doesn't work on someone higher than me.")

        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False

        # Now permission check
        if member.id in owners:
            if ctx.author.id not in owners:
                return await ctx.error(f"Sorry, but {ctx.command.name} doesn't work on the dev m8.")
            else:
                pass
        if member.id == ctx.guild.owner.id:
            return await ctx.error(f"Sorry, but {ctx.command.name} doesn't work on the owner.")
        if ctx.author.top_role == member.top_role:
            return await ctx.error(f"Sorry, but {ctx.command.name} doesn't work on someone who is equal in power to oneself.")
        if ctx.author.top_role < member.top_role:
            return await ctx.error(f"Sorry, but {ctx.command.name} doesn't work on someone higher than you.")
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
