import discord
from discord.ext import commands

class Tokumei(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tokumei")
    async def tokumei_dm_command(self, ctx, *, message: str = None):
        """DM限定：匿名メッセージ送信機能"""
        anon_channel_id = 1376785231960346644
        log_channel_id = 1377479769687330848

        # DM以外からの実行は拒否
        if ctx.guild is not None:
            await ctx.send("⚠️ このコマンドはDMでのみ使用できます。")
            return

        # 入力チェック
        if not message:
            await ctx.send("使い方：t!tokumei [匿名で送りたいメッセージ]")
            return

        # チェック①：リンク含むか
        if "http://" in message or "https://" in message or "discord.gg" in message:
            await ctx.send("⚠️ 匿名メッセージにリンクは使えません。")
            return

        # チェック②：200文字以上
        if len(message) > 200:
            await ctx.send("⚠️ メッセージは200文字以内にしてください。")
            return

        try:
            anon_channel = self.bot.get_channel(anon_channel_id)
            if anon_channel:
                await anon_channel.send(f"📩 匿名メッセージ：\n{message}")
                await ctx.send("✅ 匿名メッセージを送信しました！")

                # ログ送信
                log_channel = self.bot.get_channel(log_channel_id)
                if log_channel:
                    embed = discord.Embed(title="📋 匿名メッセージログ", color=discord.Color.orange())
                    embed.add_field(name="送信者", value=f"{ctx.author}（{ctx.author.id}）", inline=False)
                    embed.add_field(name="内容", value=message, inline=False)
                    await log_channel.send(embed=embed)
            else:
                await ctx.send("⚠️ 送信チャンネルが見つかりませんでした。")

        except Exception as e:
            await ctx.send(f"⚠️ エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(Tokumei(bot))
