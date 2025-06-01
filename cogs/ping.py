import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        # ✅ コマンドが完全一致 "t!ping" でない場合は無視（エラーメッセージなし）
        if ctx.message.content.strip() != "t!ping":
            return

        # ✅ レイテンシ計測（ms単位に変換）
        latency = round(self.bot.latency * 1000)

        # ✅ 応答速度を表示するEmbed作成
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Botの応答速度は `{latency}ms` です。",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

# ✅ CogとしてBotに登録
async def setup(bot):
    await bot.add_cog(PingCog(bot))
