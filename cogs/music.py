import discord
import typing
import ksoftapi
import base64
from discord.ext import commands, tasks
from jishaku.paginators import WrappedPaginator, PaginatorEmbedInterface
from utils import usefull

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.ksoft = self.bot.ksoft

	# Cough cough https://github.com/FireDiscordBot/bot/blob/master/cogs/ksoft.py
	@commands.command(name="lyrics", aliases=["ly"], usage="[search result index] <song name>")
	async def lyrics_command(self, ctx, songIndex: typing.Optional[int] = 0, *, query):
		songs = None
		async with usefull.Slow(ctx):
			try:
				songs = await self.ksoft.music.lyrics(query)
			except ksoftapi.NoResults:
				return await ctx.warn(f"No lyrics found for {query}")
		song = songs[songIndex]
		b64_song_name = base64.b64encode(song.name.encode("ascii"))
		paginator = WrappedPaginator(prefix="", suffix="", max_size=1000)
		for line in song.lyrics.split("\n"):
			paginator.add_line(line)
		embed = discord.Embed(color=ctx.author.color, title=f"{song.artist} - {song.name}", url=f"https://lyrics.ksoft.si/song/{song.id}/{b64_song_name}")
		embed.set_thumbnail(url=song.album_art)
		footer = {
			"text": "Powered by KSoft.Si",
			"icon_url": "https://cdn.ksoft.si/images/Logo128.png"
		}
		interface = PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author, embed=embed)
		await interface.send_to(ctx)


def setup(bot):
	bot.add_cog(Music(bot))
