import discord
import ksoftapi
import logging
import os
import json
import datetime
import time
from utils import permissions, usefull
from discord.ext import commands

c = usefull.colors

class EpicContext(commands.Context):
	pass

class Robot(commands.Bot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config = usefull.load("config.json")
		self.ksoft = ksoftapi.Client(self.config.ksoft_token)
		# Languages!
		self.langs = ["en"]
		self.strings = {}
		for lang in self.langs:
			try:
				self.strings[lang] = usefull.load(f"languages/{lang}.json")
				print(f"loaded language {lang}")
			except Exception as err:
				print(f"error loading language {lang}: {err}")

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
		try:
			await self.change_presence(
				activity=discord.Activity(
					type=activity_types.get(activity_type, 0),
					name=activity_name
				),
				status=status_type
			)
			print(f"Set presence to: [{status_color_code}{status_type}{c.END}] {c.BOLD}{activity_type.upper()} {activity_name.upper()}{c.END}")
		except Exception as err:
			print(f"Error setting status: {err}")

	async def on_ready(self):
		print(f"Logged in to discord as {self.user.name}#{self.user.discriminator}")
		perms_int = 2146958847
		print(f"Add me you your server with this url: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions={perms_int}")
		await self.update_presence()

	async def on_message(self, msg):
		if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
			return
		ctx = await self.get_context(msg, cls=EpicContext)
		await self.invoke(ctx)
