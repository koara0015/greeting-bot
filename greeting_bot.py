# ✅ 必要なライブラリをインポート
import discord                    # Discordの機能を使うため
import os                         # 環境変数からトークンを取得するため
import random                     # ランダム処理（例：おみくじなど）に使う
import asyncio                    # 非同期処理に必要（sleepなど）
from datetime import datetime     # 日時処理（例：起動時間）
from discord.ext import commands  # Botコマンドを使うための拡張
from discord import app_commands  # スラッシュコマンド用

# ✅ トークンを環境変数から取得（セキュリティのため）
TOKEN = os.getenv("DISCORD_TOKEN")

# ✅ 必要な意図（intents）を設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージ内容を扱えるようにする
intents.presences = True        # ステータス取得用
intents.members = True          # メンバー情報取得用

# ✅ Bot本体を作成
client = commands.Bot(command_prefix="t!", intents=intents, help_command=None)
tree = client.tree  # スラッシュコマンド登録用

# ✅ 起動時刻の記録（例：稼働時間計算などに使える）
start_time = datetime.now()

# ✅ おみくじの使用履歴（1日1回制限の管理）
omikuji_usage = {}

# ✅ クールダウン管理（例：t!yamu制限）
yamu_cooldowns = {}

# ✅ 各種ID設定
notify_channel_id = 1371322394719031396  # 起動・ログ通知用チャンネル
react_channel_id = 1125349326269452309   # 👍リアクション対象チャンネル
owner_id = 1150048383524941826           # BotオーナーID

# 管理者／モデレーター／VIPのIDリスト（将来の権限管理にも活用可能）
admin_ids = [1150048383524941826, 1095693259403173949]
moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412, 1138810816905367633]
vip_ids = [1150048383524941826]

# ✅ Bot起動時に実行される処理
@client.event
async def on_ready():
    await tree.sync()  # スラッシュコマンドを同期
    print(f'ログインしました：{client.user}')

    # 起動通知をチャンネルに送信
    channel = client.get_channel(notify_channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ 通知チャンネルが見つかりません")

# ✅ コマンド実行時のエラー処理（ユーザーへの通知とログ記録）
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ 引数が足りません。コマンドの使い方を確認してください。")
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

# ✅ メッセージ受信時の処理（手動コマンドとDMのハンドリング）
@client.event
async def on_message(message):
    # Bot自身のメッセージは無視
    if message.author.bot:
        return

    # ✅ DMでの処理：t!tokumei だけは許可、他は無視
    if isinstance(message.channel, discord.DMChannel):
        if message.content.strip().split()[0] == "t!tokumei":
            pass  # Cogで処理するため通過
        else:
            return  # その他のDMメッセージは無視

    # ✅ t!shutdown（オーナー専用）
    if message.content.strip().split()[0] == "t!shutdown":
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ t!restart（オーナー専用）
    if message.content.strip().split()[0] == "t!restart":
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("再起動をしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ 存在しないコマンドのチェック（コマンド名が一致するか）
    if message.content.startswith("t!"):
        command_name = message.content.strip().split()[0]  # 最初の単語だけ取り出す
        known_prefixes = [
            't!help', 't!say', 't!shutdown', 't!restart', 't!omikuji',
            't!yamu', 't!ai', 't!user', 't!stats', 't!mittyan', 't!serverinfo',
            't!admin', 't!dm', 't!chatgpt', 't!tokumei', 't!avatar', 't!ping'
        ]
        if command_name not in known_prefixes:
            await message.channel.send("❌ そんなコマンドはありません。[t!help]で確認してください。")
            return

    # ✅ Cog側に処理を渡す（正式コマンドのみ）
    await client.process_commands(message)

# ✅ Cogの読み込み（各機能を分離して管理）
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
    await client.load_extension("cogs.unknown_command")

# ✅ トークン未設定時のエラーチェック
if not TOKEN:
    print("❌ エラー: DISCORD_TOKEN が設定されていません。")
    exit()

# ✅ Botを起動！
client.run(TOKEN)
