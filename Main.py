import os
try:
    import discord
except ModuleNotFoundError:
    os.system('pip install -r requirements.txt')
    import discord
import asyncio
import sys
from discord.ext.commands.errors import CommandInvokeError, CommandError, BadArgument
from discord.ext import commands
from discord.ext.commands import AutoShardedBot as a
from os import listdir
from os.path import isfile, join
import traceback
import time
import datetime
import settings
settings = settings.set()
bot = a(command_prefix='..')


@bot.event
async def on_ready():
    print("=" * 50)
    print('{0.user} 계정에 로그인 하였습니다!'.format(bot))
    print("=" * 50)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandInvokeError):
        return await ctx.send('에러가 발생하였습니다!')
    if isinstance(error, BadArgument):
        return await ctx.send('그 채널혹은 유저혹은 역할을 찾이 못하였습니다!')

cogs_dir = "cogs"
for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

bot.run(settings.token)
