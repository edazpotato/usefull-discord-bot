from discord.ext import commands

class UserPrefrences():
	"""A class that takes a discord.User object and returns an object with their preferences"""
	def __init__(self, bot, user):
		self.user = user
		self.bot = bot
		self._language = "en" # TEMPORARY until I get the DB going
		self._color = 0xff0000 # TEMPORARY until I get the DB going

	@property
	def language(self):
		return self._language

	@property
	def color(self):
		return self._color

class GuildPrefrences():
	"""A class that takes a discord.Guild object and returns an object with their preferences"""
	def __init__(self, bot, guild):
		self.guild = guild
		self.bot = bot
		self._language = "en" # TEMPORARY until I get the DB going
		self._prefix = self.bot.config.prefixes[0] # TEMPORARY until I get the DB going
	
	@property
	def language(self):
		return self._language

	@property
	def prefix(self):
		return self._prefix

class CtxConfig():
	def __init__(self, context):
		self.ctx = context
		self._author = UserPrefrences(self.ctx.bot, self.ctx.author)
		self._guild = GuildPrefrences(self.ctx.bot, self.ctx.guild)

	@property
	def author(self):
		return self._author

	@property
	def guild(self):
		return self._guild

class Context(commands.Context):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.emoji = self.bot.config.emoji
		# Preferences
		self.config = CtxConfig(self)
		self._language = "en"
		if self.config.guild.language is not None:
			self._language = self.config.guild.language
		if self.config.author.language is not None:
			self._language = self.config.author.language

	async def error(self, msg: str, **kwargs):
		await self.send(f"{self.emoji.no} {msg}", **kwargs)
	async def warning(self, msg: str, **kwargs):
		await self.send(f"{self.emoji.maybe} {msg}", **kwargs)
	async def success(self, msg: str, **kwargs):
		await self.send(f"{self.emoji.yes} {msg}", **kwargs)

	@property
	def language(self):
		return self._language

	@property
	def strings(self):
		return self.bot.strings[self._language]