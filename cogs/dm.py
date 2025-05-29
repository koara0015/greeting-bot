import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="dm")
    async def dm_command(self, ctx, user_arg: str = None, *, message: str = None):
        """管理者専用：ユーザーにDMを送信します"""
        admin_ids = [1150048383524941826, 1095693259403173949]  # 管理者ID
        notify_channel_id = 1371322394719031396  # ログチャンネルID

        if ctx.author.id not in admin_ids:
            await ctx.send("🛑 管理者専用コマンドです。")
            return

        if not user_arg or not message:
            await ctx.send("使い方：t!dm [ユーザーID または メンション] [メッセージ]")
            return

        # メンションをIDに変換
        if user_arg.startswith("<@") and user_arg.endswith(">"):
            user_arg = user_arg.replace("<@", "").replace("!", "").replace(">", "")

        try:
            user_id = int(user_arg)
            dm_user = await self.bot.fetch_user(user_id)

            if len(message) > 500:
                await ctx.send("⚠️ メッセージが長すぎます（500文字以内にしてください）。")
                return

            await dm_user.send(message)
            await ctx.send(f"✅ ユーザー {dm_user.name} にDMを送信しました。")

            # ログ送信
            log_channel = self.bot.get_channel(notify_channel_id)
            if log_channel:
                embed = discord.Embed(
                    title="📩 DM送信ログ",
                    color=discord.Color.dark_blue()
                )
                embed.add_field(name="実行者", value=f"{ctx.author}（{ctx.author.id}）", inline=False)
                embed.add_field(name="送信先", value=f"{dm_user}（{dm_user.id}）", inline=False)
                embed.add_field(name="メッセージ内容", value=message, inline=False)
                await log_channel.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ DMの送信に失敗しました: {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))
