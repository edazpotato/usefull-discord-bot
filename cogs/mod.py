import discord
import datetime
from discord.ext import commands, tasks
from utils import permissions

action_colors = {
	"alert": 0xe32f0b,
	"warning": 0xe37e0b,
	"ok": 0x4ce30b,
	"info": 0x0b7be3
}

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

def actionReason(action, mod, member, reason=None):
	if reason is None:
		reason = "no reason given."
	return f"{member.id} was {action}ed by {mod.id} for {reason}"

async def actionEmbed(ctx, action, mod, member, reason, severity="info"):
	embed = discord.Embed()
	embed.color = action_colors[severity]
	embed.title = action
	embed.description = self.actionReason(self, action, mod, member, reason)
	embed.timestamp = datetime.datetime.utcnow()
	embed.add_field(name="Offender", value=f"`{member}`\n`{member.id}`", inline=True)
	embed.add_field(name="Offence", value=reason)
	embed.add_field(name="Moderator", value=f"`{mod}`\n`{mod.id}`", inline=True)
	embed.add_field(name="Punishment", value=action)
	return await ctx.send(embed=embed)

class Moderation(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="kick")
	@permissions.bot_has_permissions(kick_members=True)
	@permissions.author_has_permissions(kick_members=True)
	async def kick_comamnd(self, ctx, member: discord.Member, *, reason: ModActionReason=None):
		if await permissions.check_priv(ctx, member):
			return
		await member.kick(reason=actionReason("kick", ctx.author, member, reason))
		await self.actionEmbed(ctx, "kick", ctx.author, member, reason, "warning")

	@commands.command(name="ban", aliases=["banish"])
	@permissions.bot_has_permissions(ban_members=True)
	@permissions.author_has_permissions(ban_members=True)
	async def ban_command(self, ctx, member: discord.Member, *, reason: ModActionReason=None):
		if await permissions.check_priv(ctx, member):
			return
		#await member.ban(reason=actionReason("ban", ctx.author, member, reason))
		await self.actionEmbed(ctx, "ban", ctx.author, member, reason, "alert")

	@commands.command(name="unban", aliases=["unbanish"])
	@permissions.bot_has_permissions(ban_members=True)
	@permissions.author_has_permissions(ban_members=True)
	async def unban_command(self, ctx, user: discord.User, *, reason: ModActionReason=None):
		try:
			await ctx.guild.fetch_ban(user)
		except discord.NotFound as err:
			return await ctx.error(ctx.strings.ERR_CANNOT_UNBAN_NOT_BANNED_MEMBER)
		await member.unban(reason=actionReason("ban", ctx.author, member, reason))
		await self.actionEmbed(ctx, "unban", ctx.author, member, reason, "ok")


def setup(bot):
    bot.add_cog(Moderation(bot))
