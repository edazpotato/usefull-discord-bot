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
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_SELF.format(ctx))
        if member.id == ctx.bot.user.id:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT.format(ctx))

        # Check if the bot can do stuff
        if ctx.guild.me == member.top_role:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT_EQUAL.format(ctx))
        if ctx.guild.me < member.top_role:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT_HIGHER.format(ctx))

        # Now permission check
        if member.id in owners:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_BOT_OWNER.format(ctx))

        # Check if user bypasses
        if (ctx.author.id == ctx.guild.owner.id) or (ctx.author.id in owners):
            return False

        if member.id == ctx.guild.owner.id:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_GUILD_OWNER.format(ctx))
        if ctx.author.top_role == member.top_role:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_AUTHOR_EQUAL.format(ctx))
        if ctx.author.top_role < member.top_role:
            return await ctx.error(ctx.strings.ERR_MOD_CANNOT_PUNNISH_AUTHOR_HIGHER.format(ctx))
        return False
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
