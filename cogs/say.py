import discord
from discord.ext import commands

# SayCommand というクラスを作り、Cog（機能のかたまり）として定義します
class SayCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Botインスタンスを受け取って保持します

    # 「t!say」という名前のコマンドを定義します
    @commands.command(name="say")
    async def say_command(self, ctx):
        # 設定（オーナーIDやモデレーターID、ログチャンネルなど）
        owner_id = 1150048383524941826
        moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412, 1138810816905367633]
        notify_channel_id = 1371322394719031396

        # メッセージをスペース区切りで分割（最大3つ）
        parts = ctx.message.content.split(' ', 2)
        if len(parts) < 3:
            await ctx.send("使い方：t!say [チャンネルID or #チャンネル] [メッセージ]")
            return

        # モデレーター権限があるかチェック
        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # 送信先チャンネルの取得（メンション or ID）
        target_channel = None
        if ctx.message.channel_mentions:
            # メンションで指定されたチャンネル
            target_channel = ctx.message.channel_mentions[0]
            if ctx.author.id != owner_id and target_channel.guild.id != ctx.guild.id:
                await ctx.send("⚠️ 他のサーバーのチャンネルには送信できません。")
                return
        else:
            # チャンネルIDで指定された場合
            try:
                channel_id = int(parts[1])
                target_channel = self.bot.get_channel(channel_id)
                if ctx.author.id != owner_id and target_channel and target_channel.guild.id != ctx.guild.id:
                    await ctx.send("⚠️ 他のサーバーのチャンネルには送信できません。")
                    return
            except:
                await ctx.send("⚠️ チャンネルIDの形式が正しくありません。")
                return

        # チャンネルが見つからなかった場合
        if not target_channel:
            await ctx.send("⚠️ チャンネルが見つかりませんでした")
            return

        # メッセージ本文取得
        message_text = parts[2]

        # リンクや文字数オーバーをチェック
        has_link = any(link in message_text for link in ["http://", "https://", "www.", "discord.gg"])
        too_long = len(message_text) > 200

        if has_link:
            await ctx.send("⚠️ リンクが含まれているため却下しました。")
            return

        if too_long:
            await ctx.send("⚠️ メッセージが長すぎます（200文字以内にしてください）。")
            return

        # 実際に送信する処理とログ送信
        try:
            await target_channel.send(message_text)  # 対象チャンネルに送信
            await ctx.send("✅ メッセージを送信しました")  # 実行者に通知

            # ログを記録（埋め込み形式）
            log_channel = self.bot.get_channel(notify_channel_id)
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

# Bot本体からこのファイルを読み込むための関数（必須！）
async def setup(bot):
    await bot.add_cog(SayCommand(bot))
