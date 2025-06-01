import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        # ✅ 修正：完全一致以外はエラーメッセージを返すようにする
        if ctx.message.content.strip() != "t!ping":
            await ctx.send("❌ 正しい使い方でコマンドを入力してください。[t!help]で確認できます。")
            return

        # ✅ Botの遅延時間（応答速度）をミリ秒単位で取得
        latency = round(self.bot.latency * 1000)

        # ✅ 埋め込みメッセージを作成して送信
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Botの応答速度は `{latency}ms` です。",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

# ✅ Bot起動時にこのCogを読み込むように設定
async def setup(bot):
    await bot.add_cog(PingCog(bot))
