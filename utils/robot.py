import discord
import ksoftapi
import logging
import os
import json
import datetime
import time
from utils import permissions, usefull
from discord.ext import commands
from collections import namedtuple

c = usefull.colors

class EpicContext(commands.Context):
	async def error(self, msg: str, **kwargs):
		await self.send(f"{self.bot.emoji.no} {msg}", **kwargs)
	async def warning(self, msg: str, **kwargs):
		await self.send(f"{self.bot.emoji.maybe} {msg}", **kwargs)
	async def success(self, msg: str, **kwargs):
		await self.send(f"{self.bot.emoji.yes} {msg}", **kwargs)

	@property
	def lang(self):
		return self.bot.langs[0]

	@property
	def strings(self):
		return self.bot.strings[self.lang]

class Robot(commands.AutoShardedBot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config = usefull.load("config.json")
		self.ksoft = ksoftapi.Client(self.config.ksoft_token)
		# Languages!
		self.langs = ["en"]
		self.strings = {}
		self.load_langs()
		self.emoji = self.config.emoji

	def load_langs(self):
		for lang in self.langs:
			try:
				self.strings[lang] = usefull.load(f"languages/{lang}.json")
				print(f"{c.OKCYAN}Loaded language {c.OKBLUE}{lang}{c.END}")
			except Exception as err:
				print(f"{c.FAIL}Error loading language {c.WARNING}{lang}{c.END}: {err}")

	async def update_presence(self, activity_type=None, activity_name=None, status_type=None):
		# Use defualts if they aren't provided
		if (activity_type is None):
			activity_type = self.config.activity_type
		if (activity_name is None):
			activity_name = self.config.activity
		if (status_type is None):
			status_type = self.config.status_type

		# Set a colour code for console output
		status_color_code = c.OKBLUE
		if (status_type == "online"):
			status_color_code = c.OKGREEN
		elif status_type== "idle":
			status_color_code = c.WARNING
		else:
			status_color_code = c.FAIL

		activity_types = {"listening": 2, "watching": 3, "competing": 5}
		activity_num = activity_types.get(activity_type, 0)
		activity_name_extra = ""
		if activity_num == 5:
			activity_name_extra = " in"
		try:
			await self.change_presence(
				activity=discord.Activity(
					type=activity_num,
					name=activity_name
				),
				status=status_type
			)
			print(f"{c.OKCYAN}Set presence to:{c.END} [{status_color_code}{status_type}{c.END}] {c.BOLD}{activity_type.upper()+activity_name_extra} {activity_name}{c.END}")
		except Exception as err:
			print(f"{c.FAIl}Error setting status{c.END}: {err}")

	async def handle_commands(self, msg):
		if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
			return
		ctx = await self.get_context(msg, cls=EpicContext)
		await self.invoke(ctx)

	async def on_ready(self):
		print(f"{c.OKCYAN}Logged in to discord as {c.OKBLUE}{self.user.name}#{self.user.discriminator}{c.END}")
		perms_int = 2146958847
		print(f"{c.OKCYAN}Add me you your server with this url: {c.OKGREEN}https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions={perms_int}{c.END}")
		await self.update_presence()

	async def on_message(self, msg):
		await self.handle_commands(msg)

	async def on_message_edit(self, before, after):
		if before.content == after.content:
			return
		await self.handle_commands(after)
