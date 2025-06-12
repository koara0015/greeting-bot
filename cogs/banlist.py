import discord
from discord.ext import commands

class BanList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="banlist")
    async def banlist(self, ctx):
        # ✅ オーナーまたは管理者のみ使用可
        if ctx.author.id not in self.bot.owner_ids and ctx.author.id not in self.bot.admin_ids:
            await ctx.send("🛑 このコマンドはオーナーまたは管理者のみ使用できます。")
            return

        try:
            bans = []
            async for ban in ctx.guild.bans():  # ✅ 非同期ジェネレーターの正しい使い方
                bans.append(ban)

            if not bans:
                await ctx.send("✅ 現在、BANされているメンバーはいません。")
                return

            # ✅ 25件ずつEmbedで送信
            chunk_size = 25
            for i in range(0, len(bans), chunk_size):
                chunk = bans[i:i+chunk_size]

                embed = discord.Embed(
                    title="⛔ BANされたメンバー一覧",
                    description=f"{len(bans)} 件のBAN記録があります。",
                    color=discord.Color.red()
                )

                for ban_entry in chunk:
                    user = ban_entry.user
                    reason = ban_entry.reason or "理由なし"
                    embed.add_field(
                        name=f"{user}（ID: {user.id}）",
                        value=f"理由: {reason}",
                        inline=False
                    )

                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ BANリストの取得中にエラーが発生しました: {e}")

# ✅ Cog登録
async def setup(bot):
    await bot.add_cog(BanList(bot))
