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
            return await ctx.send(f"Sorry, but you can't {ctx.command.name} yourself.")
        if member.id == ctx.bot.user.id:
            return await ctx.send("No u")

        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False

        # Now permission check
        if member.id in owners:
            if ctx.author.id not in owners:
                return await ctx.send(f"Sorry, but {ctx.command.name} doesn't work on the dev m8.")
            else:
                pass
        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"Sorry, but {ctx.command.name} doesn't work on the owner m8.")
        if ctx.author.top_role == member.top_role:
            return await ctx.send(f"Sorry, but {ctx.command.name} doesn't work on someone who is equal in power to oneself.")
        if ctx.author.top_role < member.top_role:
            return await ctx.send(f"Sorry, but {ctx.command.name} doesn't work on someone higher than you.")
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
