import discord
import os
from boto.s3.connection import S3Connection

TOKEN = S3Connection(os.environ['TOKEN'], os.environ['TOKEN'])


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}!'.format(self.user))
    
    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


client = MyClient()
client.run(TOKEN)
