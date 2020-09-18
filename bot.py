import discord

class Client(discord.Client):
    async def on_ready(self):
        print(f"Logged in to discord as {self.user.name}#{self.user.tag}")
        print(f"Add me you your server with this url: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot&permissions=2146958847")

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(os.getEnv("DISCORD_TOKEN"))