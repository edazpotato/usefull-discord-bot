import discord
import ksoftapi
import logging
import os
from utils import permissions
from discord.ext import commands

class Robot(commands.Bot):

	def __init__(self,*args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ksoft = ksoftapi.Client(os.getenv("KSOFT_TOKEN"))


	async def on_ready(self):
		print(f"Logged in to discord as {self.user.name}#{self.user.discriminator}")
		print(f"Add me you your server with this url: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=2146958847")
		await self.change_presence(activity=discord.Game("with goodness knows what?"))

	async def on_message(self, msg):
		if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
			return
		await self.process_commands(msg)