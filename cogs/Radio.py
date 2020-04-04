from discord import Embed, Colour
from discord.ext.commands import command, Cog, check, group
from discord.utils import get
from asyncio import TimeoutError
from cogs.utils.dataIO import dataIO
import os

class Radio(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = 'data/radio/status.json'
        self.data = dataIO.load_json(self.file)
        self.file2 = 'data/radio/settings.json'
        self.data2 = dataIO.load_json(self.file2)

    @group(name='settings', pass_context=True, aliases=['ㄴㄷㅅ샤ㅜㅎㄴ', 'tjfwjd', '설정'])
    async def settings(self, ctx):
        if ctx.invoked_subcommand is None:
            em = Embed(colour=0xffff00)
            em.add_field(name='라디오 관리자 설정', value='DJ - 라디오 DJ역할을 설정합니다!\n알람 - 라디오 시작할때 시작을 알릴 멘션을 선택합니다!\n채널 - 라디오 보이스 채널을 설정합니다!')
            return await ctx.send(embed=em)


    @group(name='radio', pass_context=True, aliases=['ㄱㅁ야ㅐ', 'fkeldh', '라디오'])
    async def radio(self, ctx):
        if ctx.invoked_subcommand is None:
            em = Embed(colour=0xffff00)
            em.add_field(name='라디오 DJ 설정', value='시작 - 라디오를 시작합니다!\n종료 - 라디오를 종료합니다!\n예약 - 라디오를 예약합니다!\n취소 - 라디오의 예약 취소합니다!')
            return await ctx.send(embed=em)

    @radio.command(name='시작', no_pm=True)
    async def start(self, ctx, *, message=None):
        author = ctx.author
        server = ctx.guild
        await ctx.message.delete()
        if author.voice == None:
            return await ctx.send('> 라디오 시작전 보이스 채널에 입장해주세요!')
        if not self.data.get(str(server.id)) == None:
            return await ctx.send('> 현재 진행중인 라디오가 있습니다! 현재는 예약만 가능합니다!')
        if message == None:
            message = f'{author.name} 님의 라디오가 시작합니다!'
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
            return await a.edit(content='> 라디오를 시작하겠습니다!')
        if str(reaction.emoji) == '❌':
            return await a.edit(content='> 라디오 시작을 취소하였습니다!')
        self.data[str(ctx.guild.id)] = {}
        self.data[str(ctx.guild.id)].update({"dj": author.id})
        dataIO.save_json(self.file, self.data)

    @radio.command(name='종료', no_pm=True)
    async def 종료(self, ctx, *, message=None):
        author = ctx.author
        server = ctx.guild
        await ctx.message.delete()
        if author.voice == None:
            return await ctx.send('> 라디오 시작전 보이스 채널에 입장해주세요!')
        if not self.data.get(str(server.id)) == None:
            return await ctx.send('> 현재 진행중인 라디오가 있습니다! 현재는 예약만 가능합니다!')
        if message == None:
            message = f'{author.name} 님의 라디오가 시작합니다!'

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
