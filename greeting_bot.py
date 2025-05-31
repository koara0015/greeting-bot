# ✅ 必要なライブラリをインポート
import discord
import os
import random
import asyncio
from datetime import datetime
from discord.ext import commands
from discord import app_commands

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
moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412, 1138810816905367633]
vip_ids = [1150048383524941826]

# ✅ Bot起動時の処理
@client.event
async def on_ready():
    await tree.sync()
    print(f'ログインしました：{client.user}')

    # 起動通知の送信
    channel = client.get_channel(notify_channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ 通知チャンネルが見つかりません")

# ✅ コマンド実行時のエラー処理（CommandNotFoundはunknown_commandで処理）
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ 引数が足りません。コマンドの使い方を確認してください。")
    elif isinstance(error, commands.CommandNotFound):
        return  # 存在しないコマンドは unknown_command.py に任せる
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🛑 必要な権限がありません。")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("⚠️ コマンドの実行中にエラーが発生しました。")
        notify_channel = client.get_channel(notify_channel_id)
        if notify_channel:
            await notify_channel.send(f"🔴 コマンドエラー: `{error.original}`")
        print(f"Command error: {error.original}")
    else:
        await ctx.send("⚠️ 予期しないエラーが発生しました。")
        notify_channel = client.get_channel(notify_channel_id)
        if notify_channel:
            await notify_channel.send(f"⚠️ 不明なエラー: `{error}`")
        print(f"Unhandled error: {error}")

# ✅ メッセージ受信時の処理（DMと特定コマンド処理）
@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author.bot:
        return

    # ✅ DMで「t!tokumei」のみ許可
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith("t!tokumei"):
            pass  # Cogに処理を渡す
        else:
            return  # その他のDMメッセージは無視

    # ✅ t!shutdown（完全一致のみ実行）
    if message.content.strip() == "t!shutdown":
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ t!restart（完全一致のみ実行）
    if message.content.strip() == "t!restart":
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("再起動をしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ その他のメッセージをコマンドとして処理
    await client.process_commands(message)

# ✅ Cogの読み込み（機能ごとに整理）
@client.event
async def setup_hook():
    await client.load_extension("cogs.ping")
    await client.load_extension("cogs.say")
    await client.load_extension("cogs.dm")
    await client.load_extension("cogs.tokumei")
    await client.load_extension("cogs.ai")
    await client.load_extension("cogs.user")
    await client.load_extension("cogs.admin")
    await client.load_extension("cogs.yamu")
    await client.load_extension("cogs.serverinfo")
    await client.load_extension("cogs.stats")
    await client.load_extension("cogs.chatgpt")
    await client.load_extension("cogs.mittyan")
    await client.load_extension("cogs.omikuji")
    await client.load_extension("cogs.help")
    await client.load_extension("cogs.autoresponder")
    await client.load_extension("cogs.reaction")
    await client.load_extension("cogs.unknown_command")  # 存在しないコマンドの処理を任せる

# ✅ トークン未設定時のエラーチェック
if not TOKEN:
    print("❌ エラー: DISCORD_TOKEN が設定されていません。")
    exit()

# ✅ Botを起動！
client.run(TOKEN)
