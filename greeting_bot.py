# ✅ 必要なライブラリをインポート
import discord
import os
import random
import asyncio
import logging  # ← 追加
from datetime import datetime
from discord.ext import commands
from discord import app_commands

# ✅ loggingの設定（ログをターミナルやファイルに出力したいとき便利！）
logging.basicConfig(
    level=logging.INFO,  # INFOレベル以上のログを表示
    format="%(asctime)s [%(levelname)s] %(message)s",  # 表示フォーマット
    datefmt="%Y-%m-%d %H:%M:%S"  # 日付フォーマット
)

# ✅ トークンを環境変数から取得（セキュリティのため）
TOKEN = os.getenv("DISCORD_TOKEN")

# ✅ 必要な意図（intents）を設定
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# ✅ Bot本体を作成（コマンドプレフィックスは「t!」、ヘルプは自作のためNone）
client = commands.Bot(command_prefix="t!", intents=intents, help_command=None)
tree = client.tree

# ✅ 起動時刻の記録
start_time = datetime.now()

# ✅ 使用履歴やクールダウンの管理辞書
omikuji_usage = {}
yamu_cooldowns = {}

# ✅ 各種ID
notify_channel_id = 1371322394719031396
react_channel_id = 1125349326269452309
owner_id = 1150048383524941826

admin_ids = [1150048383524941826, 1095693259403173949]
moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412]
vip_ids = [1150048383524941826]

# ✅ Cogのリスト（再起動時にも使う）
cogs_list = [
    "cogs.ping",
    "cogs.say",
    "cogs.dm",
    "cogs.tokumei",
    "cogs.ai",
    "cogs.user",
    "cogs.admin",
    "cogs.yamu",
    "cogs.serverinfo",
    "cogs.stats",
    "cogs.chatgpt",
    "cogs.mittyan",
    "cogs.omikuji",
    "cogs.help",
    "cogs.autoresponder",
    "cogs.reaction",
    "cogs.unknown_command"
]

# ✅ Bot起動時の処理
@client.event
async def on_ready():
    await tree.sync()
    logging.info(f'ログインしました：{client.user}')  # ← loggingで出力
    channel = client.get_channel(notify_channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            logging.warning(f"チャンネルへの送信に失敗しました: {e}")  # ← warningで出力
    else:
        logging.warning("⚠️ 通知チャンネルが見つかりません")

# ✅ エラー処理
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ 引数が足りません。")
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🛑 権限がありません。")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("⚠️ コマンド実行中にエラーが発生しました。")
        logging.error(f"Command error: {error.original}")  # ← errorログ
        channel = client.get_channel(notify_channel_id)
        if channel:
            await channel.send(f"🔴 コマンドエラー: `{error.original}`")
    else:
        await ctx.send("⚠️ 不明なエラーが発生しました。")
        logging.error(f"Unhandled error: {error}")  # ← errorログ
        channel = client.get_channel(notify_channel_id)
        if channel:
            await channel.send(f"⚠️ 不明なエラー: `{error}`")

# ✅ メッセージ受信時の処理
@client.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("t!tokumei"):
            pass
        else:
            return

    if message.content.strip() == "t!shutdown":
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            logging.info("Botがシャットダウンされました")  # ← infoログ
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    if message.content.strip() == "t!restart":
        if message.author.id == owner_id:
            success = []
            failed = []

            for cog in cogs_list:
                try:
                    await client.unload_extension(cog)
                    await client.load_extension(cog)
                    success.append(cog)
                except Exception as e:
                    failed.append(f"{cog} → {e}")
                    logging.error(f"❌ {cog} の再読み込みに失敗: {e}")  # ← エラーログ

            msg = f"🔁 Cogの再読み込みが完了しました。\n✅ 成功: {len(success)} 件\n❌ 失敗: {len(failed)} 件"
            await message.channel.send(msg)

            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send(msg)

            logging.info("🔁 再起動コマンドによるCog再読み込み完了")  # ← infoログ
            return
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
            return

    await client.process_commands(message)

# ✅ 最初のCog読み込み処理
@client.event
async def setup_hook():
    for cog in cogs_list:
        try:
            await client.load_extension(cog)
            logging.info(f"✅ Cogロード成功: {cog}")  # ← infoログ
        except Exception as e:
            logging.error(f"❌ Cogロード失敗: {cog} → {e}")  # ← errorログ

# ✅ トークン未設定チェック
if not TOKEN:
    logging.critical("❌ エラー: DISCORD_TOKEN が設定されていません。")  # ← criticalログ
    exit()

# ✅ Botを起動！
client.run(TOKEN)
