import discord
import typing
import ksoftapi
from discord.ext import commands, tasks
from jishaku.paginators import WrappedPaginator, PaginatorEmbedInterface
from utils import usefull

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ksoft = self.bot.ksoft

	# Cough cough https://github.com/FireDiscordBot/bot/blob/master/cogs/ksoft.py
	@commands.command(name="lyrics")
	async def lyrics(self, ctx, songIndex: typing.Optional[int] = 0, *, query):
		songs = None
		async with usefull.Slow(ctx):
			try:
				songs = await self.ksoft.music.lyrics(query)
			except ksoftapi.NoResults:
				return await ctx.warn(f"No lyrics found for {query}")
		song = songs[songIndex]
		paginator = WrappedPaginator(prefix="", suffix="", max_size=1000)
		for line in song.lyrics.split("\n"):
			paginator.add_line(line)
		embed = discord.Embed(color=ctx.author.color, title=f"{lyrics.artist} - {lyrics.name}", url=lyrics.url)
		embed.set_thumbnail(url=lyrics.album_art)
		footer = {
			"text": "Powered by KSoft.Si",
			"icon_url": "https://cdn.ksoft.si/images/Logo128.png"
		}
		interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author, _embed=embed, _footer=footer)
		await interface.send_to(ctx)


def setup(bot):
	bot.add_cog(Music(bot))
