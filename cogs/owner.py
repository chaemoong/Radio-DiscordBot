"""Coding: UTF-8, Coding by: Discord Tag: 뭉개구름#9454"""
import discord
import datetime
import inspect
import os
import time
from pytz import timezone, utc
from discord import Spotify
from discord.ext import commands
from cogs.utils.dataIO import dataIO
from discord import VoiceRegion
from discord import Game
from discord.utils import get
from copy import deepcopy
import asyncio
import settings
settings = settings.set()

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def is_owner(ctx):
        return ctx.author.id == settings.owner

    @commands.command(pass_context=True)
    @commands.check(is_owner)
    async def cmd(self, ctx, *, code=None):
        """eval 시킵니다!"""
        result = None
        global_vars = globals().copy()
        global_vars['self'] = self
        global_vars['bot'] = self.bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.guild
        if not code == None:
            if 'os' in code or 'shutdown' in code or 'webbrowser' in code or 'base64' in code:
                embed = discord.Embed(title='Success...?', colour=0x6bffc8, timestamp=datetime.datetime.utcnow())
                embed.add_field(name=':inbox_tray: **INPUT**', value='```py\n' + str(code) + '\n```', inline=False)
                embed.add_field(name=':outbox_tray: **OUTPUT**', value='```하지만 어림도 없지```', inline=False)
                return await ctx.send(embed=embed)
        try:
            python = '```py\n{}\n```'
            res = eval(code, global_vars)
            if inspect.isawaitable(res):
                result = await res
            else:
                result = res
        except Exception as e:
            embed = discord.Embed(title='Error', colour=0xef6767, timestamp=datetime.datetime.utcnow())
            embed.add_field(name=':inbox_tray: **INPUT**', value='```py\n' + f'{code}' + '\n```', inline=False)
            embed.add_field(name=':outbox_tray: **OUTPUT**', value=python.format(type(e).__name__ + ': ' + str(e)), inline=False)
            return await ctx.send(embed=embed)
            
        embed = discord.Embed(title='Success', colour=0x6bffc8, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=':inbox_tray: **INPUT**', value='```py\n' + str(code) + '\n```', inline=False)
        embed.add_field(name=':outbox_tray: **OUTPUT**', value=python.format(result), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.check(is_owner)
    async def load(self, ctx, cogs):
        """cogs를 리로드 하는 명령어 입니다!"""
        try:
            self.bot.load_extension(cogs)
            return await ctx.send('그 기능이 로드 되었습니다!')
        except discord.ext.commands.errors.ExtensionAlreadyLoaded:
            return await ctx.send('그 기능이 이미 로드 되어있습니다!')
        except discord.ext.commands.errors.ExtensionNotFound:
            return await ctx.send('그 기능을 찾을수 없습니다!')
        except Exception as e:
            print(e)
            return await ctx.send('그 기능을 로드 되는중 오류가 발생하였습니다!\n터미널이나 콘솔을 확인해주세요!')
        except:
            return await ctx.send('그 기능을 찾을수 없습니다!')

    @commands.command()
    @commands.check(is_owner)
    async def reload(self, ctx, cogs):
        """cogs를 리로드 하는 명령어 입니다!"""
        try:
            self.bot.reload_extension('cogs.' + cogs)
            await ctx.send('그 기능이 리로드 되었습니다!')
        except discord.ext.commands.errors.ExtensionNotLoaded:
            if cogs == 'music':
                self.bot.load_extension(cogs)
            else:
                self.bot.load_extension('cogs.' + cogs)
            await ctx.send('그 기능이 리로드 되었습니다!')
        except Exception as e:
            print(e)
            await ctx.send('그 기능이 리로드 되는중 오류가 발생하였습니다!\n터미널이나 콘솔을 확인해주세요!')
        except:
            await ctx.send('그 기능을 찾을수 없습니다!')
        
def setup(bot):
    bot.add_cog(Owner(bot))

