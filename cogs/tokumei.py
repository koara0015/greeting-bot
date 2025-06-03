# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands
from discord import app_commands
import random

# ✅ Tokumei クラス（Cogとして定義）
class Tokumei(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # main.py の client を受け取って保持

    # ✅ サーバー上で t!tokumei が使われたときの注意メッセージ
    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            not isinstance(message.channel, discord.DMChannel)
            and message.content.startswith("t!tokumei")
            and not message.author.bot
        ):
            await message.channel.send(
                "📬 このコマンドはDMで使ってください！\n"
                "例：Botに `t!tokumei 明日テストいやだ` と送ると、匿名で投稿されます。"
            )

    # ✅ 通常コマンド（DM専用）
    @commands.command(name="tokumei")
    async def tokumei_dm_command(self, ctx, *, message: str = None):
        """DM限定：匿名メッセージ送信機能"""

        # ✅ サーバー上では使えないよう制限
        if ctx.guild is not None:
            await ctx.send("⚠️ このコマンドはDMでのみ使用できます。")
            return

        # ✅ 引数がない場合
        if not message:
            await ctx.send("使い方：t!tokumei [匿名で送りたいメッセージ]")
            return

        # ✅ リンク制限・文字数制限
        if "http://" in message or "https://" in message or "discord.gg" in message:
            await ctx.send("⚠️ 匿名メッセージにリンクは使えません。")
            return
        if len(message) > 200:
            await ctx.send("⚠️ メッセージは200文字以内にしてください。")
            return

        try:
            # ✅ 投稿チャンネルとログチャンネルの取得（configから）
            anon_channel = self.bot.get_channel(self.bot.anon_channel_id)
            log_channel = self.bot.get_channel(self.bot.anon_log_channel_id)

            if anon_channel:
                # ✅ ランダムな名前・アイコン
                names = ["匿名A", "匿名B", "匿名C", "名無し", "？？？", "無名さん", "スラッシュコマンドで失礼します"]
                icons = ["https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png"]
                anon_name = random.choice(names)
                anon_icon = random.choice(icons)

                # ✅ Webhook経由で送信
                webhook = await anon_channel.create_webhook(name=anon_name)
                await webhook.send(message, avatar_url=anon_icon)
                await webhook.delete()

                await ctx.send("✅ 匿名メッセージを送信しました！")

                # ✅ ログチャンネルに送信
                if log_channel:
                    embed = discord.Embed(title="📋 匿名メッセージログ", color=discord.Color.orange())
                    embed.add_field(name="送信者", value=f"{ctx.author}（{ctx.author.id}）", inline=False)
                    embed.add_field(name="内容", value=message, inline=False)
                    await log_channel.send(embed=embed)
            else:
                await ctx.send("⚠️ 送信チャンネルが見つかりませんでした。")

        except Exception as e:
            await ctx.send(f"⚠️ エラーが発生しました: {e}")

    # ✅ スラッシュコマンド版（全員使用可）
    @app_commands.command(name="tokumei", description="匿名でメッセージを送信します（全員可）")
    @app_commands.describe(message="匿名で投稿したいメッセージ内容")
    async def tokumei_slash_command(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        # ✅ 入力内容チェック
        if "http://" in message or "https://" in message or "discord.gg" in message:
            await interaction.followup.send("⚠️ 匿名メッセージにリンクは使用できません。")
            return
        if len(message) > 200:
            await interaction.followup.send("⚠️ 匿名メッセージは200文字以内で送ってください。")
            return

        try:
            # ✅ チャンネル取得（configから）
            anon_channel = self.bot.get_channel(self.bot.anon_channel_id)
            log_channel = self.bot.get_channel(self.bot.anon_log_channel_id)

            # ✅ ランダムな名前とアイコン
            names = ["匿名A", "匿名B", "匿名C", "名無し", "？？？", "無名さん", "スラッシュコマンドで失礼します"]
            icons = ["https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png"]
            anon_name = random.choice(names)
            anon_icon = random.choice(icons)

            # ✅ Webhook送信
            webhook = await anon_channel.create_webhook(name=anon_name)
            await webhook.send(message, avatar_url=anon_icon)
            await webhook.delete()

            await interaction.followup.send("✅ 匿名メッセージを送信しました！")

            # ✅ ログに送信
            if log_channel:
                embed = discord.Embed(title="📋 匿名メッセージログ", color=discord.Color.orange())
                embed.add_field(name="送信者", value=f"{interaction.user}（{interaction.user.id}）", inline=False)
                embed.add_field(name="内容", value=message, inline=False)
                await log_channel.send(embed=embed)

        except Exception as e:
            print(f"Webhookエラー: {e}")
            await interaction.followup.send("⚠️ 投稿に失敗しました。管理者にご連絡ください。")

# ✅ CogとしてBotに登録
async def setup(bot):
    await bot.add_cog(Tokumei(bot))
