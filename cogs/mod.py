import discord
import datetime
from discord.ext import commands, tasks
from utils import permissions

# Utils from https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id


class ModActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(f'reason is too long ({len(argument)}/{reason_max})')
        return ret


class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	async def actionEmbed(self, ctx, action, mod, member, reason="No offence given."):
		embed = discord.Embed()
		embed.title = action
		embed.description = f"{member} was {action}ed for {reason}"
		embed.timestamp = datetime.datetime.utcnow()
		embed.add_field(name="Offender", value=f"`{member}`\n`{member.id}`")
		embed.add_field(name="Offence", value=reason)
		embed.add_field(name="Moderator", value=f"`{mod}`\n`{mod.id}`")
		embed.add_field(name="Punsihment", value=action)
		return await ctx.send(embed=embed)

	def actionReason(self, action, mod, member, reason="no reason given."):
		return f"{member.id} was kicked by {mod.id} for {reason}"

	@commands.command()
	@permissions.bot_has_permissions(kick_members=True)
	@permissions.author_has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, *, reason: ModActionReason="no reason provided."):
		if await permissions.check_priv(ctx, member) == True:
			return
		await member.kick(reason=self.actionReason("kick", ctx.author, member, reason))
		await self.actionEmbed(ctx, "kick", ctx.author, member, reason)


def setup(bot):
    bot.add_cog(Moderation(bot))
