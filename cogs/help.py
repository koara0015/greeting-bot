# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

# ✅ Help クラス（Cog）
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # main.pyのclientを受け取る

    @commands.command(name="help", help="利用可能なコマンドの一覧を表示します（モデレーター以上）")
    async def help_command(self, ctx):
        # ✅ 完全一致でないメッセージは無視
        if ctx.message.content.strip() != "t!help":
            return

        # ✅ モデレーター以上のIDまたは管理者権限かをチェック
        if ctx.author.id not in self.bot.moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ Embedを作成
        embed = discord.Embed(
            title="📘 ヘルプ - コマンド一覧",
            description="たまごのお部屋専用Botコマンド一覧です。\n`t!コマンド名` で実行できます。",
            color=discord.Color.blurple()
        )

        # ✅ 各カテゴリごとにコマンドを追加（手動で記述）
        embed.add_field(
            name="🛠 管理系コマンド",
            value=(
                "`t!say [チャンネル] [内容]` - 指定チャンネルにメッセージ送信\n"
                "`t!dm [ユーザー] [内容]` - 指定ユーザーにDM送信\n"
                "`t!yamu [チャンネル]` - 病み構文を送信（0.1秒ごと）\n"
                "`t!shutdown` - Botを終了（オーナーのみ）\n"
                "`t!restart` - Cogを再読み込み（オーナーのみ）"
            ),
            inline=False
        )

        embed.add_field(
            name="💬 ユーザー系コマンド",
            value=(
                "`t!ping` - 応答速度を表示\n"
                "`t!avatar [@ユーザー]` - アバター画像を表示\n"
                "`t!omikuji` - おみくじ（1日1回）\n"
                "`t!ai [メッセージ]` - なんちゃってAI返信\n"
                "`t!serverinfo` - サーバー情報を表示\n"
                "`t!stats` - 使用統計を表示"
            ),
            inline=False
        )

        embed.add_field(
            name="🕵️ 匿名系コマンド",
            value=(
                "`t!tokumei [メッセージ]` - DMで匿名投稿\n"
                "`/tokumei` - スラッシュ版匿名投稿"
            ),
            inline=False
        )

        await ctx.send(embed=embed)

# ✅ Cogとして登録する関数
async def setup(bot):
    await bot.add_cog(Help(bot))
