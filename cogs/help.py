# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

# ✅ Help クラス（Cog）
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Botインスタンス（main.pyのclient）を保持

    # ✅ t!help コマンド定義
    @commands.command(name="help", help="利用可能なコマンドの一覧を表示します（モデレーター以上）")
    async def help_command(self, ctx):
        # ✅ 完全一致でないメッセージは無視
        if ctx.message.content.strip() != "t!help":
            return

        # ✅ 権限チェック（モデレーター以上のID or 管理者権限）
        if ctx.author.id not in self.bot.moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ Embedメッセージ作成（コマンド一覧）
        embed = discord.Embed(
            title="📘 コマンド一覧",
            description="現在使用可能なコマンドの一覧です。\n`t!コマンド名` で実行できます。",
            color=discord.Color.green()
        )

        # ✅ Botに登録されたコマンドから一覧を取得
        for command in self.bot.commands:
            if command.hidden:
                continue  # hidden=True のコマンドは除外
            embed.add_field(
                name=f"🟢 t!{command.name}",
                value=command.help or "（説明なし）",
                inline=False
            )

        await ctx.send(embed=embed)

# ✅ Cogとして登録する関数
async def setup(bot):
    await bot.add_cog(Help(bot))
