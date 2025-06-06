# ✅ 必要なライブラリをインポート
import discord
import os
import random
import asyncio
import logging
import json
from datetime import datetime
from discord.ext import commands
from discord import app_commands

# ✅ loggingの設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ✅ トークンを取得
TOKEN = os.getenv("DISCORD_TOKEN")

# ✅ intentsを設定
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# ✅ config.jsonを読み込む
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

client = commands.Bot(command_prefix=config["command_prefix"], intents=intents, help_command=None)
tree = client.tree
client.config = config

# ✅ チャンネルIDを保持
client.notify_channel_id = config.get("notify_channel_id")
client.react_channel_id = config.get("react_channel_id")
client.tokumei_channel_id = config.get("tokumei_channel_id")
client.tokumei_log_channel_id = config.get("tokumei_log_channel_id")

# ✅ 起動時間記録・辞書
start_time = datetime.now()
omikuji_usage = {}
yamu_cooldowns = {}

# ✅ ids.jsonを読み込む
with open("ids.json", "r", encoding="utf-8") as f:
    ids_data = json.load(f)

client.owner_ids = ids_data.get("owner", [])
client.admin_ids = ids_data.get("admin", [])
client.moderator_ids = ids_data.get("moderator", [])
client.vip_ids = ids_data.get("vip", [])

# ✅ Bot起動時の処理
@client.event
async def on_ready():
    await tree.sync()
    logging.info(f'ログインしました：{client.user}')
    channel = client.get_channel(client.notify_channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            logging.warning(f"チャンネルへの送信に失敗: {e}")
    else:
        logging.warning("通知チャンネルが見つかりません")

# ✅ 通常コマンドのエラー処理
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
        logging.error(f"Command error: {error.original}")
        channel = client.get_channel(client.notify_channel_id)
        if channel:
            await channel.send(f"🔴 コマンドエラー: `{error.original}`")
    else:
        await ctx.send("⚠️ 不明なエラーが発生しました。")
        logging.error(f"Unhandled error: {error}")
        channel = client.get_channel(client.notify_channel_id)
        if channel:
            await channel.send(f"⚠️ 不明なエラー: `{error}`")

# ✅ スラッシュコマンドのエラー処理（クールダウン対策あり）
@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        # ※ tokumei.py 側で既に処理してるので何もしない
        return
    logging.error(f"スラッシュコマンドエラー: {error}")
    channel = client.get_channel(client.notify_channel_id)
    if channel:
        await channel.send(f"⚠️ スラッシュコマンドエラー: `{error}`")

# ✅ メッセージ受信時の処理
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # ✅ DMのt!tokumei以外は無視
    if isinstance(message.channel, discord.DMChannel):
        if not message.content.startswith("t!tokumei"):
            return

    # ✅ シャットダウン
    if message.content.strip() == "t!shutdown":
        if message.author.id in client.owner_ids:
            channel = client.get_channel(client.notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            logging.info("Botがシャットダウンされました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ 再起動（Cog再読み込み）
    if message.content.strip() == "t!restart":
        if message.author.id in client.owner_ids:
            success = []
            failed = []

            for cog in os.listdir("./cogs"):
                if cog.endswith(".py") and not cog.startswith("_"):
                    cog_name = f"cogs.{cog[:-3]}"
                    try:
                        await client.unload_extension(cog_name)
                        await client.load_extension(cog_name)
                        success.append(cog_name)
                    except Exception as e:
                        failed.append(f"{cog_name} → {e}")
                        logging.error(f"❌ {cog_name} の再読み込み失敗: {e}")

            msg = f"🔁 Cogの再読み込みが完了しました。\n✅ 成功: {len(success)} 件\n❌ 失敗: {len(failed)} 件"
            await message.channel.send(msg)
            channel = client.get_channel(client.notify_channel_id)
            if channel:
                await channel.send(msg)
            logging.info("再起動コマンドによるCogの再読み込み完了")
            return
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
            return

    await client.process_commands(message)

# ✅ Cog自動読み込み
@client.event
async def setup_hook():
    for cog in os.listdir("./cogs"):
        if cog.endswith(".py") and not cog.startswith("_"):
            cog_name = f"cogs.{cog[:-3]}"
            try:
                await client.load_extension(cog_name)
                logging.info(f"✅ Cogロード成功: {cog_name}")
            except Exception as e:
                logging.error(f"❌ Cogロード失敗: {cog_name} → {e}")

# ✅ トークンチェック
if not TOKEN:
    logging.critical("❌ エラー: DISCORD_TOKEN が設定されていません。")
    exit()

# ✅ Bot起動！
client.run(TOKEN)
