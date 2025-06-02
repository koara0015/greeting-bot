# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

# ✅ SayCommand クラス（Cog）
class SayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Botインスタンス（main.pyのclient）を保持

    # ✅ t!say コマンドの定義
    @commands.command(name="say")
    async def say_command(self, ctx):
        # ✅ コマンドが "t!say" と完全一致しない場合は無視
        if ctx.message.content.split(' ')[0] != "t!say":
            return

        # ✅ コマンドの引数分割（最大3つ）
        parts = ctx.message.content.split(' ', 2)
        if len(parts) < 3:
            await ctx.send("使い方：t!say [チャンネルID or #チャンネル] [メッセージ]")
            return

        # ✅ モデレーター以上かチェック（ID一覧は main.py から受け取ったもの）
        if ctx.author.id not in self.bot.moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ 送信先チャンネルの取得（メンションまたはチャンネルID）
        target_channel = None
        if ctx.message.channel_mentions:
            target_channel = ctx.message.channel_mentions[0]
            if ctx.author.id not in self.bot.owner_ids and target_channel.guild.id != ctx.guild.id:
                await ctx.send("⚠️ 他のサーバーのチャンネルには送信できません。")
                return
        else:
            try:
                channel_id = int(parts[1])
                target_channel = self.bot.get_channel(channel_id)
                if ctx.author.id not in self.bot.owner_ids and target_channel and target_channel.guild.id != ctx.guild.id:
                    await ctx.send("⚠️ 他のサーバーのチャンネルには送信できません。")
                    return
            except:
                await ctx.send("⚠️ チャンネルIDの形式が正しくありません。")
                return

        if not target_channel:
            await ctx.send("⚠️ チャンネルが見つかりませんでした")
            return

        # ✅ メッセージ本文を取得
        message_text = parts[2]

        # ✅ リンク・文字数チェック
        has_link = any(link in message_text for link in ["http://", "https://", "www.", "discord.gg"])
        too_long = len(message_text) > 200

        if has_link:
            await ctx.send("⚠️ リンクが含まれているため却下しました。")
            return
        if too_long:
            await ctx.send("⚠️ メッセージが長すぎます（200文字以内にしてください）。")
            return

        # ✅ メッセージ送信とログ
        try:
            await target_channel.send(message_text)
            await ctx.send("✅ メッセージを送信しました")

            log_channel = self.bot.get_channel(1371322394719031396)  # 通知チャンネル固定ID
            if log_channel:
                embed = discord.Embed(title="📤 t!say 実行ログ", color=discord.Color.green())
                embed.add_field(name="実行者", value=f"{ctx.author} (ID: {ctx.author.id})", inline=False)
                embed.add_field(name="送信先", value=f"{target_channel.name}（ID: {target_channel.id}）", inline=False)
                embed.add_field(name="サーバー", value=f"{target_channel.guild.name}", inline=False)
                embed.add_field(name="送信内容", value=message_text, inline=False)
                embed.add_field(name="リンク含む？", value="✅ はい" if has_link else "❌ いいえ", inline=True)
                embed.add_field(name="文字数オーバー？", value="✅ はい" if too_long else "❌ いいえ", inline=True)
                await log_channel.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ エラーが発生しました: {e}")

# ✅ Cog登録用関数（BotがこのCogを読み込む時に呼ばれる）
async def setup(bot):
    await bot.add_cog(SayCommand(bot))
