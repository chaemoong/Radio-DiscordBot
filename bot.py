from discord.ext.commands.errors import CommandNotFound
import discord
from discord.ext.commands import AutoShardedBot as a
from os import listdir
from os.path import isfile, join
import traceback

bot = a(command_prefix='!!')

@bot.event
async def on_ready():
    print("=" * 50)
    print('{0.user} 계정에 로그인 하였습니다!'.format(bot))
    print("=" * 50)

@bot.event
async def on_message(message):
    if message.guild == None:
        guild = 'DIRECT MESSAGE'
    else: guild = message.guild.name
    print(f'{guild} | |USER: {message.author} | CONTENT: {message.content}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return

cogs_dir = "cogs"
for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'{extension} 모듈이 로드 되었습니다!')
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

bot.run('TOKEN')
