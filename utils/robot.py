import discord
import ksoftapi
import logging
import os
import datetime
import time
from utils import permissions, usefull
from discord.ext import commands

class Robot(commands.Bot):

	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config = usefull.load("config.json")
		self.ksoft = ksoftapi.Client(self.config.ksoft_token)


	async def on_ready(self):
		print(f"Logged in to discord as {self.user.name}#{self.user.discriminator}")
		perms_int = 2146958847
		print(f"Add me you your server with this url: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions={perms_int}")
		activity_types = {"listening": 2, "watching": 3, "competing": 5}
		await self.change_presence(
			activity=discord.Activity(
				type=activity_types.get(self.config.activity_type, 0),
				name=self.config.activity
			),
			status=self.config.status_type
		)

	async def on_message(self, msg):
		if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
			return
		await self.process_commands(msg)
