import discord
from discord.ext import commands
import random

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Bot自身や他のBotのメッセージは無視
        if message.author.bot:
            return

        # コマンドメッセージや空白は無視
        if message.content.startswith("t!") or not message.content.strip():
            return

        # 小文字にして処理
        text = message.content.lower()

        if "おはよ" in text:
            responses = [
                'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
                '学校行けよ',
                '寝坊してない？( ˘⁠ω˘ )',
                '早起き過ぎ！？！？！？！',
                'おっそ',
            ]
            await message.channel.send(random.choice(responses))

        elif "おやすみ" in text:
            responses = [
                'おやすみ',
                'いい夢見てね！',
                '今日もnukeされずに済んだね！',
                'おやすみのnukeは？',
                'おつかれさま、ゆっくり休んでね〜',
                'おやすみ〜',
                'もう起きてこなくていいよ',
            ]
            await message.channel.send(random.choice(responses))

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))
