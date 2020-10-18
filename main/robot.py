import discord
import ksoftapi
import logging
import os
import json
import datetime
import time
import sys
from utils import permissions, usefull
from main import context
from discord.ext import commands
from collections import namedtuple

c = usefull.colors

class Robot(commands.AutoShardedBot):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Load config
		self.config = usefull.load("config.json")
		# Ksoft.Si wrapper
		self.ksoft = ksoftapi.Client(self.config.ksoft_token)
		# Languages!
		self.langs = []
		self.strings = {}
		self.load_languages()
		# Emojis
		self.emoji = self.config.emoji
		# Development enviorment?
		self.dev = False
		# was a command line arg passed?
		# yes this is a bad way to do this. Too bad
		if (len(sys.argv) > 1):
			self.dev = True
		print(f"{c.OKCYAN}Dev env:                              {c.OKBLUE}{str(self.dev)}{c.END}")
	def load_languages(self):
		self.langs = usefull.load(f"languages/langs.json")
		for lang in self.langs:
			try:
				self.strings[lang.code] = usefull.load(f"languages/{lang.code}.json")
				print(f"{c.OKCYAN}Loaded language:                      {c.OKBLUE}{lang.name}{c.END}")
			except Exception as err:
				print(f"{c.FAIL}Error loading language: {c.WARNING}{lang.name}{c.END}: {err}")

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
			activity_name_extra = " IN"
		try:
			await self.change_presence(
				activity=discord.Activity(
					type=activity_num,
					name=activity_name
				),
				status=status_type
			)
			print(f"{c.OKCYAN}Set presence to:                      {c.END}[{status_color_code}{status_type}{c.END}] {c.BOLD}{activity_type.upper()+activity_name_extra} {activity_name}{c.END}")
		except Exception as err:
			print(f"{c.FAIl}Error setting status:{c.END} {err}")

	# handele commands yes
	async def handle_commands(self, msg):
		if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
			return
		ctx = await self.get_context(msg, cls=context.Context)
		await self.invoke(ctx)

	# events
	async def on_ready(self):
		print(f"{c.OKCYAN}Logged in to discord as:              {c.OKBLUE}{self.user.name}#{self.user.discriminator}{c.END}")
		perms_int = 2146958847
		print(f"{c.OKCYAN}Add me you your server with this url: {c.OKGREEN}https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions={perms_int}{c.END}")
		await self.update_presence()

	async def on_message(self, msg):
		await self.handle_commands(msg)

	async def on_message_edit(self, before, after):
		if before.content == after.content:
			return
		await self.handle_commands(after)
