# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

class BanList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ banlistコマンド（オーナー/アドミン限定）
    @commands.command(name="banlist")
    async def banlist(self, ctx):
        # ✅ 実行者がオーナー or アドミンかを確認
        author_id = ctx.author.id
        if author_id not in self.bot.owner_ids and author_id not in self.bot.admin_ids:
            await ctx.send("🛑 このコマンドはオーナーまたはアドミンのみ使用できます。")
            return

        await ctx.send("📋 BANリストを取得中です...")

        try:
            # ✅ 非同期ジェネレーターなので、async for で回収
            bans = [entry async for entry in ctx.guild.bans()]

            if not bans:
                await ctx.send("✅ 現在BANされているユーザーはいません。")
                return

            embed = discord.Embed(title="🚫 BANユーザー一覧", color=discord.Color.red())

            for entry in bans:
                user = entry.user
                reason = entry.reason if entry.reason else "理由不明"
                embed.add_field(
                    name=f"{user}（{user.id}）",
                    value=f"理由: {reason}",
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ BANリストの取得中にエラーが発生しました: {e}")
            print(f"[BANLIST] エラー: {e}")

# ✅ Cog登録
async def setup(bot):
    await bot.add_cog(BanList(bot))
