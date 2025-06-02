# ✅ 必要なライブラリをインポート
import discord
import os
import random
import asyncio
import logging  # ← loggingを使用して情報を出力
import json  # ← ids.json 読み込み用
from datetime import datetime
from discord.ext import commands
from discord import app_commands

# ✅ loggingの設定（ログをターミナルやRailwayログで確認可能）
logging.basicConfig(
    level=logging.INFO,  # INFOレベル以上を表示
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# ✅ トークンを環境変数から取得（.envにDISCORD_TOKENを設定する）
TOKEN = os.getenv("DISCORD_TOKEN")

# ✅ Discordの意図（intents）を設定
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# ✅ Bot本体を作成（接頭辞はt!）
client = commands.Bot(command_prefix="t!", intents=intents, help_command=None)
tree = client.tree

# ✅ 起動時間記録
start_time = datetime.now()

# ✅ 使用履歴などの辞書
omikuji_usage = {}
yamu_cooldowns = {}

# ✅ 固定のチャンネルID
notify_channel_id = 1371322394719031396
react_channel_id = 1125349326269452309

# ✅ ids.jsonを読み込んで各種IDをセット
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
    channel = client.get_channel(notify_channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            logging.warning(f"チャンネルへの送信に失敗: {e}")
    else:
        logging.warning("通知チャンネルが見つかりません")

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
        logging.error(f"Command error: {error.original}")
        channel = client.get_channel(notify_channel_id)
        if channel:
            await channel.send(f"🔴 コマンドエラー: `{error.original}`")
    else:
        await ctx.send("⚠️ 不明なエラーが発生しました。")
        logging.error(f"Unhandled error: {error}")
        channel = client.get_channel(notify_channel_id)
        if channel:
            await channel.send(f"⚠️ 不明なエラー: `{error}`")

# ✅ メッセージ受信時の処理
@client.event
async def on_message(message):
    if message.author.bot:
        return

    # DMメッセージの処理
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("t!tokumei"):
            pass
        else:
            return

    # シャットダウン処理
    if message.content.strip() == "t!shutdown":
        if message.author.id in client.owner_ids:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            logging.info("Botがシャットダウンされました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # 再起動処理（Cogを再読み込み）
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
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send(msg)
            logging.info("再起動コマンドによるCogの再読み込み完了")
            return
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
            return

    await client.process_commands(message)

# ✅ Cogの自動読み込み
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
