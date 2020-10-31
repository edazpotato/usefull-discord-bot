import typing
import urllib
import discord
import re
import json
import asyncio
from dateutil import parser
from discord.ext import commands
from utils import permissions
from utils import usefull

class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="meme", aliases=["meymey", "reddit", "subreddit", "red"], usage="[weather or not to delete the message] [subreddit]")
	async def meme_command(self, ctx, delete: typing.Optional[bool]=False, *, subreddit: typing.Optional[str]=None):
		meme = {}
		if (subreddit is not None) and (subreddit.startswith("r/")):
			subreddit = subreddit[2:]
		async with usefull.Slow(ctx):
			try:
				if subreddit is not None:
					remove_nsfw = True
					if permissions.is_nsfw(ctx):
						remove_nsfw = False
					try:
						meme = await self.bot.ksoft.images.random_reddit(subreddit, remove_nsfw=remove_nsfw, span="month")
					except:
						return await ctx.error(ctx.strings.ERR_MEME_COULDNT_GET_NON_NSFW)
				else:
					meme = await self.bot.ksoft.images.random_meme()
				if meme.nsfw and not permissions.is_nsfw(ctx):
					return await ctx.error(ctx.strings.ERR_MEME_COULDNT_GET_NON_NSFW)
			except Exception as err:
				return await ctx.error(err)#ctx.error(ctx.strings.ERR_MEME_SUBREDDIT_NOT_FOUND)
		if not meme.title:
				return await ctx.error(ctx.strings.ERR_MEME_SUBREDDIT_NOT_FOUND)
		datetime = parser.parse(str(meme.created_at)[:2]) # idk why but it wont parse unless i remove the last two chars
		embed = discord.Embed(title=meme.title, url=meme.source, color=ctx.config.author.color, timestamp=datetime)
		embed.set_image(url=meme.image_url)
		embed.set_footer(icon_url="https://cdn.ksoft.si/images/Logo128.png", text=f'Powered by KSoft.Si | 👍 {meme.upvotes} 👎 {meme.downvotes} | ' + ctx.strings.MEME_POSTED_BY_ON.format(meme.author, meme.subreddit))
		msg = await ctx.send(embed=embed)
		if delete:
			try:
				await ctx.message.delete()
			except:
				pass
			await asyncio.sleep(10)
			await msg.delete()

	@commands.command(name="urbandictionary", aliases=["urban", "ud"], usage="[weather or not to delete the message] [search result index] <word/phrase to define>")
	async def urbandictionary_command(self, ctx, delete: typing.Optional[bool]=False, index: typing.Optional[int]=0, *, query: str):
		urlquery = urllib.parse.quote(query)
		data = {}
		async with usefull.Slow(ctx):
			try:
				res = await self.bot.http_session.get(f"https://api.urbandictionary.com/v0/define?term={urlquery}")
				data = await res.json()
			except:
				return await ctx.error(ctx.strings.ERR_URBAN_DICTIONARY_ERR.format(query))
		if len(data["list"]) < 1:
			return await ctx.error(ctx.strings.ERR_NO_URBAN_DICTIONARY_DEFINITION_FOUND.format(query))
		definition = data["list"][index]
		datetime = parser.parse(definition["written_on"])
		embed = discord.Embed(title=definition["word"], url=definition["permalink"], color=ctx.config.author.color, timestamp=datetime)
		embed.set_footer(text=f'👍 {definition["thumbs_up"]} 👎 {definition["thumbs_down"]} | ' + ctx.strings.URBAN_DEFINED_BY_AT.format(definition['author']))
		embed.add_field(name=ctx.strings.URBAN_EMBED_DEFINITION_FIELD_TITLE, value=re.sub(r'[\[\]]', "", definition["definition"]))
		embed.add_field(name=ctx.strings.URBAN_EMBED_EXAMPLE_FIELD_TITLE, value="*"+re.sub(r'[\[\]]', "", definition["example"])+"*")
		msg = await ctx.send(embed=embed)
		if delete:
			try:
				await ctx.message.delete()
			except:
				pass
			await asyncio.sleep(10)
			await msg.delete()

	@commands.command(name="mc-build", aliases=["mcbuild"])
	async def mcbuild_commmand(self, ctx):
		data = {}
		try:
			res = await self.bot.http_session.get("https://api.mcbuild.dev/catalog")
			txt = await res.text()
			data = json.loads(txt)
		except Exception as err:
			await ctx.error(ctx.strings.ERR_API)
		image = discord.File("static/mcbuild.png", filename="image.png")
		langs_str = "`" + "`, `".join(data["langs"]) + "`"
		libs_str = "`" + "`, `".join(data["libs"]) + "`"
		embed = discord.Embed(title="MC-Build packages", url="https://mcbuild.dev", color=ctx.config.author.color)
		embed.add_field(name="Languages", value=langs_str)
		embed.add_field(name="Libraries", value=libs_str)
		embed.set_thumbnail(url="attachment://image.png")
		await ctx.send(embed=embed, file=image)


def setup(bot):
	bot.add_cog(Fun(bot))
