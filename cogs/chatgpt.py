import discord
from discord.ext import commands

class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="chatgpt")
    async def chatgpt_command(self, ctx):
        """API制限で使用不可の案内（誰でも可）"""
        await ctx.send("🔴 API制限に達したため利用不可です。")

async def setup(bot):
    await bot.add_cog(ChatGPT(bot))
