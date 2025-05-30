# 必要なライブラリをインポート
import discord                    # Discordの機能全般を使用するため
import os                         # 環境変数からトークンなどを読み取るため
import random                     # ランダムな値（例：返答、おみくじなど）に使う
import asyncio                    # 非同期処理に使う（例：sleepなど）
from datetime import datetime     # 起動時刻の記録などに使用
from discord.ext import commands  # コマンド機能を扱う拡張機能
from discord import app_commands  # スラッシュコマンド用

# ユーザーごとのクールダウン管理（例：t!yamu）
yamu_cooldowns = {}

# トークンを環境変数から取得（セキュリティ対策）
TOKEN = os.getenv("DISCORD_TOKEN")

# DiscordのBotの動作に必要な「意図（intents）」を設定
intents = discord.Intents.default()
intents.message_content = True  # メッセージの内容を取得可能にする
intents.presences = True        # ユーザーのオンライン状態などを取得する
intents.members = True          # サーバーのメンバー情報を取得する

# Botの本体を作成（プレフィックスは t!）
client = commands.Bot(command_prefix="t!", intents=intents, help_command=None)
tree = client.tree  # スラッシュコマンドの登録に使用

# 起動時の時刻を記録（例：稼働時間表示に使える）
start_time = datetime.now()

# おみくじの使用記録（ユーザーIDごとの使用日を記録）
omikuji_usage = {}

# 各種設定（チャンネルIDやユーザーID）
notify_channel_id = 1371322394719031396  # 通知やログ送信用チャンネル
react_channel_id = 1125349326269452309   # 自動でリアクションを付けるチャンネル
owner_id = 1150048383524941826           # Botのオーナー（完全権限を持つ）

admin_ids = [1150048383524941826, 1095693259403173949]  # 管理者ID
moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412, 1138810816905367633]
vip_ids = [1150048383524941826]  # 将来的に特別扱いするVIPのID

# ✅ Botが起動したときに一度だけ実行される処理
@client.event
async def on_ready():
    await tree.sync()  # スラッシュコマンドをDiscordに登録
    print(f'ログインしました：{client.user}')

    # 起動通知を送る
    await client.wait_until_ready()
    channel = client.get_channel(notify_channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ 通知チャンネルが見つかりません")

# ✅ コマンド実行時のエラーを処理する（ユーザーと管理者の両方に通知）
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ 引数が足りません。コマンドの使い方を確認してください。")
    elif isinstance(error, commands.CommandNotFound):
        return  # 存在しないコマンドは unknown_command.py で処理するため無視
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

# ✅ メッセージを受け取ったときの処理
@client.event
async def on_message(message):
    # Bot自身や他のBotのメッセージは無視
    if message.author.bot:
        return

# ✅ DMでのメッセージ処理（t!tokumei だけ許可）
if isinstance(message.channel, discord.DMChannel):
    if message.content.startswith("t!tokumei"):
        pass  # そのままCogへ通す
    else:
        return  # その他のDMメッセージは無視

    # ✅ t!shutdown コマンド（オーナー専用）
    if message.content.startswith('t!shutdown'):
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ t!restart コマンド（オーナー専用）
    if message.content.startswith('t!restart'):
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("再起動をしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # ✅ 他のコマンドを処理（Cog側に渡す）
    await client.process_commands(message)

# ✅ Cogを読み込む（各機能を分割したモジュールを読み込む）
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
    await client.load_extension("cogs.unknown_command")  # 存在しないコマンドに対応

# ✅ トークンが設定されていないときの安全対策
if not TOKEN:
    print("❌ エラー: DISCORD_TOKEN が設定されていません。")
    exit()

# ✅ Botを起動！
client.run(TOKEN)
