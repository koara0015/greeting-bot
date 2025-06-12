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

        # ✅ 処理中の案内
        await ctx.send("📋 BANリストを取得中です...")

        try:
            # ✅ サーバーからBANされたユーザーのリストを取得
            bans = await ctx.guild.bans()
            if not bans:
                await ctx.send("✅ 現在BANされているユーザーはいません。")
                return

            # ✅ 表示用メッセージを作成
            embed = discord.Embed(title="🚫 BANユーザー一覧", color=discord.Color.red())

            for ban_entry in bans:
                user = ban_entry.user
                reason = ban_entry.reason if ban_entry.reason else "理由不明"
                # ⚠️ BAN日時はAPIから直接取得できないので「取得時点の表示」のみになります
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
