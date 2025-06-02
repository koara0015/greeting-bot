# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

# ✅ Adminクラス（Cog）として定義
class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Botインスタンスを保持（main.pyのclient）

    # ✅ t!dm コマンド定義
    @commands.command(name="dm")
    async def dm_command(self, ctx, user_arg: str = None, *, message: str = None):
        """管理者専用：ユーザーにDMを送信します"""

        # ✅ 権限チェック：管理者IDに含まれていなければ拒否
        if ctx.author.id not in self.bot.admin_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("🛑 管理者専用コマンドです。")
            return

        # ✅ 引数が不足している場合
        if not user_arg or not message:
            await ctx.send("使い方：t!dm [ユーザーID または メンション] [メッセージ]")
            return

        # ✅ メンションをユーザーIDに変換
        if user_arg.startswith("<@") and user_arg.endswith(">"):
            user_arg = user_arg.replace("<@", "").replace("!", "").replace(">", "")

        try:
            user_id = int(user_arg)
            dm_user = await self.bot.fetch_user(user_id)

            # ✅ 文字数制限チェック
            if len(message) > 500:
                await ctx.send("⚠️ メッセージが長すぎます（500文字以内にしてください）。")
                return

            # ✅ DM送信
            await dm_user.send(message)
            await ctx.send(f"✅ ユーザー {dm_user.name} にDMを送信しました。")

            # ✅ ログ送信
            log_channel = self.bot.get_channel(1371322394719031396)  # 通知チャンネルID（固定）
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

# ✅ Cogとして登録する関数
async def setup(bot):
    await bot.add_cog(Admin(bot))
