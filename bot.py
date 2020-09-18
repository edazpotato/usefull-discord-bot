import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in to discord as {self.user}")

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(os.getEnv("DISCORD_TOKEN"))