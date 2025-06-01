import discord
from discord.ext import commands
from datetime import datetime

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()  # Botの起動時刻を記録しておく

    @commands.command(name="stats")
    async def stats_command(self, ctx):
        """Botのステータスを表示します（モデレーター以上限定）"""

        # ✅ モデレーターID（+ 将来の拡張を考慮して複数対応）
        moderator_ids = [
            1150048383524941826,  # オーナー
            1095693259403173949,  # 管理者
            1354645428095680563,  # モデレーター
            841603812548411412,
            1138810816905367633
        ]

        # ✅ 入力コマンドが完全一致（t!stats だけ）のときだけ処理
        if ctx.message.content.strip() != "t!stats":
            return  # 余計な引数がある場合は無視（エラーも表示しない）

        # ✅ 権限チェック：IDが含まれていない＆管理者でもない場合は拒否
        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ 起動からの稼働時間を計算
        now = datetime.now()
        uptime = now - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)

        # ✅ ステータス情報をEmbedで送信
        embed = discord.Embed(
            title="📊 Botのステータス",
            color=discord.Color.purple()
        )
        embed.add_field(name="起動時間", value=f"{hours}時間 {minutes}分 {seconds}秒", inline=False)
        embed.add_field(name="コマンド数", value="現在対応しているコマンド数: 14個", inline=False)
        embed.add_field(name="ユーザー数", value=f"{len(ctx.guild.members)}人", inline=False)

        await ctx.send(embed=embed)

# ✅ Cogの登録
async def setup(bot):
    await bot.add_cog(Stats(bot))
