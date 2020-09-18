from discord.ext import commands
import ksoftapi

# Load environment variables if they aren't loaded yet
if not os.getenv("DISCORD_TOKEN"):
    from dotenv import load_dotenv
    load_dotenv()

class Client(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.ksoft = ksoftapi.Client(os.getEnv("KSOFT_TOKEN"))

	async def on_ready(self):
		print(f"Logged in to discord as {self.user.name}#{self.user.tag}")
		print(f"Add me you your server with this url: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=2146958847")

	async def on_message(self, message):
		print('Message from {0.author}: {0.content}'.format(message))

client = Client()
client.run(os.getEnv("DISCORD_TOKEN"))
