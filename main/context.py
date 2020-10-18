from discord.ext import commands

class Context(commands.Context):
	async def error(self, msg: str, **kwargs):
		await self.send(f"{self.bot.emoji.no} {msg}", **kwargs)
	async def warning(self, msg: str, **kwargs):
		await self.send(f"{self.bot.emoji.maybe} {msg}", **kwargs)
	async def success(self, msg: str, **kwargs):
		await self.send(f"{self.bot.emoji.yes} {msg}", **kwargs)

	@property
	def lang(self):
		return self.bot.langs[0].code

	@property
	def strings(self):
		return self.bot.strings[self.lang]