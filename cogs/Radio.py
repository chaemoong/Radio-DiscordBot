from discord import Embed, Colour, Role, TextChannel
from discord.ext.commands import command, Cog, check, group
from discord.utils import get
from asyncio import TimeoutError
from cogs.utils.dataIO import dataIO
import os
import asyncio
from datetime import datetime
from random import choice
import settings
settings = settings.set()
class Radio(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'data/radio/status.json'
        self.data = dataIO.load_json(self.file)
        self.file2 = 'data/radio/settings.json'
        self.data2 = dataIO.load_json(self.file2)
        self.tip = [
            '역할, 유저 관련 명령어는 제대로 안적어 주시면 봇이 아무 반응을 하지 않습니다!',
            '라디오 시작 할때 원하는 멘트로 시작할수 있어요!'
        ]

    async def is_admin(ctx):
        if ctx.author.id == settings.owner:
            return True
        if ctx.author.guild_permissions.administrator == True:
            return True
        

    @group(name='settings', no_pm=True, pass_context=True, aliases=['ㄴㄷㅅ샤ㅜㅎㄴ', 'fkeldhtjfwjd', '라디오설정'])
    async def settings(self, ctx):
        """라디오 관련 관리자 전용 명령어입니다!"""
        if ctx.invoked_subcommand is None:
            em = Embed(colour=0xffff00)
            em.add_field(name='라디오 관리자 설정', value='DJ - 라디오 DJ역할을 설정합니다!\n알람 - 라디오 시작할때 시작을 알릴 멘션을 선택합니다!\n채널 - 라디오 시작혹은 종료할때 시작 혹은 종료를 알릴 채널을 선택합니다!')
            return await ctx.send(embed=em)

    @settings.command(name='DJ', no_pm=True)
    async def DJ(self, ctx, role:Role=None):
        """라디오를 진행할 DJ를 설정하는 명령어입니다!"""
        if role == None:
            return await ctx.send(f'역할의 ID 혹은 역할의 멘션을 적어주세요!\n> TIP!: {choice(self.tip)}')
        try:
            self.data2[str(ctx.guild.id)].update({"djrole": role.id})
        except:
            self.data2[str(ctx.guild.id)] = {}
            self.data2[str(ctx.guild.id)].update({"djrole": role.id})
        dataIO.save_json(self.file2, self.data2)
        return await ctx.send(f'> `{role.name}`역할이 라디오DJ 역할이 되었습니다')

    @settings.command(name='알람', no_pm=True)
    async def alarm(self, ctx, role:Role=None):
        """라디오 알림을 알려줄 역할을 설정하는 명령어입니다!"""
        if role == None:
            return await ctx.send(f'역할의 ID 혹은 역할의 멘션을 적어주세요!\n> TIP!: {choice(self.tip)}')
        try:
            self.data2[str(ctx.guild.id)].update({"role": role.id})
        except:
            self.data2[str(ctx.guild.id)] = {}
            self.data2[str(ctx.guild.id)].update({"role": role.id})
        dataIO.save_json(self.file2, self.data2)
        return await ctx.send(f'> `{role.name}`역할이 라디오알람 역할이 되었습니다')

    @settings.command(name='채널', no_pm=True)
    async def alarmchannel(self, ctx, channel:TextChannel=None):
        """라디오 알림을 알려줄 채널을 설정하는 명령어입니다!"""
        if channel == None:
            return await ctx.send(f'역할의 ID 혹은 역할의 멘션을 적어주세요!\n> TIP!: {choice(self.tip)}')
        try:
            self.data2[str(ctx.guild.id)].update({"channel": channel.id})
        except:
            self.data2[str(ctx.guild.id)] = {}
            self.data2[str(ctx.guild.id)].update({"channel": channel.id})
        dataIO.save_json(self.file2, self.data2)
        return await ctx.send(f'> `{channel.name}`채널이 라디오알람 채널이 되었습니다')


    @group(name='radio', no_pm=True, pass_context=True, aliases=['ㄱㅁ야ㅐ', 'fkeldh', '라디오'])
    async def radio(self, ctx):
        """라디오 관련 명령어입니다!"""
        if ctx.invoked_subcommand is None:
            em = Embed(colour=0xffff00)
            em.add_field(name='라디오 DJ 설정', value='시작 - 라디오를 시작합니다!\n종료 - 라디오를 종료합니다!\n예약 - 라디오를 예약합니다!')
            return await ctx.send(embed=em)

    @radio.command(name='시작', no_pm=True)
    async def start(self, ctx, *, message=None):
        """라디오를 시작하는 명령어입니다!"""
        author = ctx.author
        server = ctx.guild
        await ctx.message.delete()
        serverdata = self.data2.get(str(server.id))
        if author.voice == None:
            return await ctx.send('> 라디오 시작전 보이스 채널에 입장해주세요!')
        if not self.data.get(str(server.id)) == {}:
            return await ctx.send('> 현재 진행중인 라디오가 있습니다! 현재는 예약만 가능합니다!')
        if serverdata == None:
            return await ctx.send(f'> 라디오 관련 데이터가 설정되있지 않습니다! `{ctx.prefix}settings`로 설정해주세요!')
        if message == None:
            message = f'{author.name} 님의 라디오가 시작합니다!'
        if not get(author.roles, id=serverdata.get('djrole')) in author.roles:
            return await ctx.send('> 라디오는 DJ만 실행시킬 수 있습니다!')
        a = await ctx.send('라디오를 시작하시겠습니까?')
        await a.add_reaction('⭕')
        await a.add_reaction('❌')
        def check(reaction, user):
            if user == author and str(reaction.emoji) == '⭕':
                return True
            if user == author and str(reaction.emoji) == '❌':
                return True
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
        except TimeoutError:
            return await a.edit(content='> 라디오 시작을 취소하였습니다!')
        if str(reaction.emoji) == '⭕':
            em = Embed(colour=0xffff00)
            em.add_field(name='라디오 시작 알림', value=message)
            await a.edit(content='> 라디오를 시작하겠습니다!')
            try:
                await self.bot.get_channel(serverdata.get('channel')).send(get(server.roles, id=serverdata.get('role')).mention, embed=em)
            except:
                return await ctx.send(f'라디오 알림 채널이 존재 하지 않습니다! `{ctx.prefix}설정`으로 설정해주세요!')
            self.data[str(ctx.guild.id)] = {}
            self.data[str(ctx.guild.id)].update({"dj": author.id})
            dataIO.save_json(self.file, self.data)
            return
        if str(reaction.emoji) == '❌':
            return await a.edit(content='> 라디오 시작을 취소하였습니다!')

    @radio.command(name='종료', no_pm=True)
    async def 종료(self, ctx):
        """라디오를 종료하는 명령어입니다!"""
        author = ctx.author
        server = ctx.guild
        await ctx.message.delete()
        serverdata = self.data2.get(str(server.id))
        if author.voice == None:
            return await ctx.send('> 라디오 종료전 보이스 채널에 입장해주세요!')
        if serverdata == None:
            return await ctx.send(f'> 라디오 관련 데이터가 설정되있지 않습니다! `{ctx.prefix}settings`로 설정해주세요!')
        if self.data.get(str(server.id)) == None or self.data.get(str(server.id)) == {}:
            a = await ctx.send('> 현재 진행중인 라디오가 없습니다!')
            await asyncio.sleep(5)
            return await a.delete()
        if not self.data[str(ctx.guild.id)]['dj'] == author.id:
            a = await ctx.send('> DJ외엔 라디오를 종료 시킬 수 없습니다!')
            await asyncio.sleep(5)
            return await a.delete()
        self.data[str(ctx.guild.id)] = {}
        dataIO.save_json(self.file, self.data)
        em = Embed(colour=0xffff00)
        em.add_field(name='라디오 종료 알림', value=f'{author.name}님의 라디오가 종료되었습니다!\nDJ분들 수고하셨습니다!')
        try:
            await self.bot.get_channel(serverdata.get('channel')).send(get(server.roles, id=serverdata.get('role')).mention, embed=em)
        except:
            return await ctx.send(f'라디오 알림 채널이 존재 하지 않습니다! `{ctx.prefix}설정`으로 설정해주세요!')
        await ctx.send('> 라디오를 종료하겠습니다!')

    @radio.command(name='예약', no_pm=True)
    async def reservation(self, ctx, time:str='1'):
        author = ctx.author
        server = ctx.guild
        await ctx.message.delete()
        if time.isdigit() == False:
            return await ctx.send('> 시간 입력란에 글을 쓰시면 안됩니다!')
        if int(time) > 12:
            return await ctx.send('> 12시간 이상을 예약 할수 없습니다!')
        today = datetime.today()
        now = datetime.now()
        radiostarttime = datetime(today.year, today.month, today.day, today.hour + int(time)) - now
        splitlist = str(radiostarttime).split(':')
        zegom = 2
        RealNum = 0
        for num in splitlist:
            await ctx.send(num)
            if len(num) > 2:
                num = num[:2]
            num = int(num)
            sleep = num * (60 ** zegom)
            zegom-= 1
            RealNum += sleep
        try:
            def check(m):
                return f'{ctx.prefix}' in m.content and '취소' in m.content and m.channel == ctx.channel and m.author == author
            msg = await self.bot.wait_for('message', check=check, timeout=RealNum)
            await ctx.send('예약이 신청되었습니다!\n> 단, 예약 취소는 불가하며 취소하시려면 기다리셔야합니다!')
        except asyncio.TimeoutError:
            if self.data.get(str(author.id)) == None:
                return
        finally:
            if not self.data.get(str(author.id)) == None or not self.data.get(str(author.id)) == {}:
                return await author.send(f'{author.name}DJ님! 이제 라디오를 시작할 시간이 되셨습니다!')

def check_folder():
    if not os.path.exists('data/radio'):
        print('data/radio 풀더생성을 완료하였습니다!')
        os.makedirs('data/radio')

def check_file():
    data = {}
    f = "data/radio/status.json"
    g = 'data/radio/settings.json'
    if not dataIO.is_valid_json(f):
        print("status.json 파일생성을 완료하였습니다!")
        dataIO.save_json(f,
                         data)
    if not dataIO.is_valid_json(g):
        print("settings.json 파일생성을 완료하였습니다!")
        dataIO.save_json(g,
                         data)

def setup(bot):
    check_folder()
    check_file()
    bot.add_cog(Radio(bot))
