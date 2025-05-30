import discord
from discord.ext import commands

class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.react_channel_id = 1125349326269452309  # 👍リアクションを付けるチャンネルのID

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return  # Botのメッセージは無視

        # 指定チャンネルに投稿されたメッセージに👍リアクションを付ける
        if message.channel.id == self.react_channel_id:
            try:
                await message.add_reaction("👍")
            except Exception as e:
                print(f"リアクション失敗: {e}")

async def setup(bot):
    await bot.add_cog(Reaction(bot))
