import discord
from discord.ext import commands
from discord import app_commands
import random

class Tokumei(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # t!tokumei（DMコマンド）
    @commands.command(name="tokumei")
    async def tokumei_dm_command(self, ctx, *, message: str = None):
        anon_channel_id = 1376785231960346644
        log_channel_id = 1377479769687330848

        if ctx.guild is not None:
            await ctx.send("⚠️ このコマンドはDMでのみ使用できます。")
            return

        if not message:
            await ctx.send("使い方：t!tokumei [匿名で送りたいメッセージ]")
            return

        if "http://" in message or "https://" in message or "discord.gg" in message:
            await ctx.send("⚠️ 匿名メッセージにリンクは使えません。")
            return

        if len(message) > 200:
            await ctx.send("⚠️ メッセージは200文字以内にしてください。")
            return

        try:
            anon_channel = self.bot.get_channel(anon_channel_id)
            if anon_channel:
                await anon_channel.send(f"📩 匿名メッセージ：\n{message}")
                await ctx.send("✅ 匿名メッセージを送信しました！")

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

    # /tokumei（スラッシュコマンド）
    @app_commands.command(name="tokumei", description="匿名でメッセージを送信します（全員可）")
    @app_commands.describe(message="匿名で投稿したいメッセージ内容")
    async def tokumei_slash_command(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        anon_channel_id = 1376785231960346644
        log_channel_id = 1377479769687330848

        if "http://" in message or "https://" in message or "discord.gg/" in message:
            await interaction.followup.send("⚠️ 匿名メッセージにリンクは使用できません。")
            return

        if len(message) > 200:
            await interaction.followup.send("⚠️ 匿名メッセージは200文字以内で送ってください。")
            return

        names = ["匿名A", "匿名B", "匿名C", "名無し", "？？？", "無名さん", "スラッシュコマンドで失礼します"]
        icons = ["https://upload.wikimedia.org/wikipedia/commons/8/89/HD_transparent_picture.png"]
        anon_name = random.choice(names)
        anon_icon = random.choice(icons)

        try:
            anon_channel = self.bot.get_channel(anon_channel_id)
            webhook = await anon_channel.create_webhook(name=anon_name)
            await webhook.send(message, avatar_url=anon_icon)
            await webhook.delete()

            await interaction.followup.send("✅ 匿名メッセージを送信しました！")

            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                embed = discord.Embed(title="匿名メッセージログ", color=discord.Color.orange())
                embed.add_field(name="送信者", value=f"{interaction.user}（{interaction.user.id}）", inline=False)
                embed.add_field(name="内容", value=message, inline=False)
                await log_channel.send(embed=embed)

        except Exception as e:
            print(f"Webhookエラー: {e}")
            await interaction.followup.send("⚠️ 投稿に失敗しました。管理者にご連絡ください。")

# Cogとして読み込む準備
async def setup(bot):
    await bot.add_cog(Tokumei(bot))
