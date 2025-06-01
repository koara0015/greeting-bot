import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """利用可能なコマンドの一覧を表示します（モデレーター以上）"""
        
        # ✅ 完全一致で「t!help」以外は無視
        if ctx.message.content.strip() != "t!help":
            return

        # ✅ モデレーター以上のID一覧
        moderator_ids = [
            1150048383524941826,  # オーナー
            1095693259403173949,  # 管理者
            1354645428095680563,  # モデレーター
            841603812548411412,
            1138810816905367633
        ]

        # ✅ 権限チェック（IDか、Discord管理者権限）
        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ Embedの作成
        embed = discord.Embed(
            title="📘 コマンド一覧",
            description="現在使用可能なコマンドの一覧です。\n`t!コマンド名` で実行できます。",
            color=discord.Color.green()
        )

        # ✅ Botに登録されたコマンドを取得
        for command in self.bot.commands:
            if command.hidden:
                continue  # hidden=True のコマンドは表示しない
            embed.add_field(
                name=f"🟢 t!{command.name}",
                value=command.help or "説明なし",
                inline=False
            )

        await ctx.send(embed=embed)

# ✅ CogとしてBotに登録
async def setup(bot):
    await bot.add_cog(Help(bot))
