import typing
import urllib.parse
import discord
from dateutil import parser
from discord.ext import commands
from utils import permissions, usefull

# Coppied from fire
region = {
    'amsterdam': '🇳🇱 Amsterdam',
    'brazil': '🇧🇷 Brazil',
    'eu-central': '🇪🇺 Central Europe',
    'eu-west': '🇪🇺 Western Europe',
    'europe': '🇪🇺 Europe',
    'frakfurt': '🇩🇪 Frankfurt',
    'hongkong': '🇭🇰 Hong Kong',
    'india': '🇮🇳 India',
    'japan': '🇯🇵 Japan',
    'england': '🇬🇧 England',
    'russia': '🇷🇺 Russia',
    'singapore': '🇸🇬 Singapore',
    'southafrica': '🇿🇦 South Africa',
    'sydney': '🇦🇺 Sydney',
    'us-central': '🇺🇸 Central US',
    'us-south': '🇺🇸 US South',
    'us-east': '🇺🇸 US East',
    'us-west': '🇺🇸 US West',
    'london': 'stop using deprecated regions >:('
}

notifs = {
    'NotificationLevel.all_messages': 'All Messages',
    'NotificationLevel.only_mentions': 'Only Mentions'
}

important_perms = {
    'administrator': 'Administrator',
    'ban_members': 'Ban',
    'change_nickname': 'Change Nickname',
    'kick_members': 'Kick',
    'manage_channels': 'Manage Channels',
    'manage_emojis': 'Manage Emojis',
    'manage_guild': 'Manage Guild',
    'manage_messages': 'Manage Messages',
    'manage_nicknames': 'Manage Nicknames',
    'manage_roles': 'Manage Roles',
    'manage_webhooks': 'Manage Webhooks',
    'mention_everyone': 'Mention Everyone',
    'view_audit_log': 'View Logs',
    'view_guild_insights': 'View Analytics',
    'attach_files': 'Send Files',
    'external_emojis': 'Use External Emojis'
}
# /Coppied from fire

class Info(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name="about", aliases=["botinfo", "robot", "bot"])
	async def botinfo_command(self, ctx):
		description =  "Hullo, "
		embed = discord.Embed(title="About me (UZX)", description=description)
		await ctx.send(embed)

	@commands.command(name="user", aliases=["userinfo", "memberinfo", "member"], usage="[user mention or id]")
	async def userinfo_command(self, ctx, user: typing.Optional[typing.Union[discord.User, discord.Member]]=None):
		if user is None:
			user = ctx.author
		member = False
		if isinstance(user, discord.Member):
			member = True
		embed = discord.Embed(title=f"Everything you need to know about {user}!") 
		perms = []
		for perm, hasperm in ctx.author.permissions_in(ctx.channel):
			if hasperm:
				if perm in important_perms:
					perms.append(important_perms[perm])
		perms_text = ", ".join(perms)
		await ctx.send(perms_text)




	@commands.command(name="server", aliases=["serverinfo", "guildinfo", "guild"])
	async def guildinfo_command(self, ctx):
		pass

	@commands.command(name="alles", aliases=["allesuserinfo", "allesinfo", "allesuser"], usage="[alles username | alles user id]")
	async def allesuserinfo_command(self, ctx, *, userid: typing.Optional[str]=None):
		if userid is None:
			return await ctx.error(ctx.strings.ERR_ALLES_ACCOUNT_NOT_LINKED)
		user = {}
		async with usefull.Slow(ctx):
			try:
				split = userid.split("#")
				if len(split) == 2:
					# username#tag
					try:
						name = urllib.parse.quote(split[0])
						if len(split[1]) != 4:
							return await ctx.error(cts.strings.ERR_ALLES_MISSING_ID_OR_NAME)
						tag = urllib.parse.quote(split[1])
						res = await self.bot.http_session.get(f"https://horizon.alles.cc/nametag/{name}/{tag}")
						iddata = await res.json()
						if "err" in iddata:
							#print(iddata["err"])
							return await ctx.error(ctx.strings.ERR_ALLES_COULDNT_GET_ID)
						userid = iddata["id"]
					except:
						return await ctx.error(ctx.strings.ERR_ALLES_COULDNT_GET_ID)
				elif len(userid) != 36:
					return await ctx.error(cts.strings.ERR_ALLES_MISSING_ID_OR_NAME)
				encodedid = urllib.parse.quote(userid)
				userres = await self.bot.http_session.get(f"https://horizon.alles.cc/users/{encodedid}")
				userdata = await userres.json()
				if "err" in userdata:
					#print(userdata["err"])
					return await ctx.error(ctx.strings.ERR_ALLES_COULDNT_GET_DATA)
				user = userdata
			except Exception as err:
				return await ctx.error(ctx.strings.ERR_ALLES_COULDNT_GET_DATA)
		dsiplayname = user["name"]
		if user["nickname"] is not None:
			dsiplayname = user["nickname"]
		plus = user["plus"]
		sparkes = ""
		description = "😢 This user doesn't has Alles Plus :("
		if plus:
			sparkes = " ✨ "
			description = "✨ This user has Alles Plus! ✨"
		embed = discord.Embed(title=f"{sparkes}{dsiplayname}{sparkes}", url=f"https://alles.cx/{user['id']}", description=description, color=ctx.config.author.color)
		embed.set_thumbnail(url=f"https://avatar.alles.cc/{user['id']}")
		embed.add_field(name="Alles ID", value=f"`{user['id']}`")
		embed.add_field(name="Name", value=f"`{user['name']}#{user['tag']}`")
		if user["username"] is not None:
			embed.add_field(name="Custom Username", value=f"`@\u200b{user['username']}`")
		await ctx.send(embed=embed)

	# Commands group that basicly runs the normal commands
	@commands.group(name="info", case_insensitive=True, invoke_without_command=True, usage="[user | server | alles]")
	async def info_command(self, ctx):
		await ctx.invoke(self.bot.get_command("about"))

	@info_command.command(name="user", aliases=["member"], usage="[user mention or id]")
	async def userinfo_subcommand(self, ctx, *, user: typing.Optional[typing.Union[discord.User, discord.Member]]=None):
		await ctx.invoke(self.bot.get_command("user"), user=user)

	@info_command.command(name="server", aliases=["guild"])
	async def guildinfo_subcommand(self, ctx):
		await ctx.invoke(self.bot.get_command("server"))

	@info_command.command(name="alles", aliases=["allesuser"], usage="[alles username | alles user id]")
	async def allesuserinfo_subcommand(self, ctx, *, userid: typing.Optional[str]=None):
		await ctx.invoke(self.bot.get_command("user"), userid=userid)

def setup(bot):
	bot.add_cog(Info(bot))