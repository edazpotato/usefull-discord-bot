import typing
import urllib
import discord
from dateutil import parser
from discord.ext import commands
from utils import permissions
# \[[^\[\]]\]

class Util(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="invite", aliases=["inv"])
	async def invite(self, ctx):
		perms_int = 2146958847
		await ctx.send(f"<https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions={perms_int}>")

	@commands.command(name="urbandictionary", aliases=["urban", "ub"])
	async def urbandictionary(self, ctx, index:typing.Optional[int]=0, *, query:str):
		urlquery = urllib.parse.quote(query)
		res = await self.bot.http_session.get(f"https://api.urbandictionary.com/v0/define?term={urlquery}")
		data = await res.json()
		if len(data["list"]) < 1:
			return await ctx.error(ctx.strings.ERR_NO_URBAN_DICTIONARY_DEFINITION_FOUND.format(query))
		definition = data["list"][index]
		datetime = parser.parse(definition["written_on"])
		embed = discord.Embed(title=definition["word"], url=definition["permalink"], color=ctx.config.author.color, timestamp=datetime)
		embed.set_footer(text=f'👍 {definition["thumbs_up"]} 👎 {definition["thumbs_down"]} | ' + ctx.strings.URBAN_DEFINED_BY_ON.format(definition['author']))
		embed.add_field(name=ctx.strings.URBAN_EMBED_DEFINITION_FIELD_TITLE, value=definition["definition"])
		embed.add_field(name=ctx.strings.URBAN_EMBED_EXAMPLE_FIELD_TITLE, value=definition["example"])
		await ctx.send(embed=embed)




def setup(bot):
	bot.add_cog(Util(bot))