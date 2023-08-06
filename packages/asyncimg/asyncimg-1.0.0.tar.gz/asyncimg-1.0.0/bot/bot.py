import discord
from discord.ext import commands


class MyBot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    async def on_ready(self):
        print(f'{str(self.user)} started')


prefix = "i."
with open('token.txt', 'r') as f:
    TOKEN = f.read()
bot = MyBot(command_prefix=prefix)

cogs = [
    'cogs.image',
]
for cog in cogs:
    try:
        bot.load_extension(cog)
    except Exception as e:
        print(e)

bot.load_extension("jishaku")

bot.run(TOKEN)
