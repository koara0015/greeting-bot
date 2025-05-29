# 必要なライブラリをインポート
import discord       # Discordの機能を使うため
import os            # トークンを環境変数から読み取るため
import random        # ランダムで返事を選ぶため
import asyncio       # 時間を待つため（sleep関数など）
from datetime import datetime
yamu_cooldowns = {}  # ユーザーIDごとのクールダウン記録

# トークンを環境変数から取得（セキュリティのため、コードに直接書かない）
TOKEN = os.getenv("DISCORD_TOKEN")

# Botの設定：メッセージの中身を読めるようにする
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True     # ユーザーのステータスを取得するために必要！
intents.members = True       # ユーザー情報を取得するために必要！

# Bot本体を作成
from discord.ext import commands  # これをインポートのところに追加！

client = commands.Bot(command_prefix="t!", intents=intents, help_command=None)

from discord import app_commands  # これもインポートに追加！
tree = client.tree

# ✅ 起動時に一度だけ記録される
start_time = datetime.now()

# おみくじの使用履歴（ユーザーID: 最後の使用日）
omikuji_usage = {}

# Botが起動したときに実行される処理
@client.event
async def on_ready():
    await tree.sync()  # ✅ スラッシュコマンドを登録！

    print(f'ログインしました：{client.user}')
    channel_id = 1371322394719031396  # 通知を送るチャンネルのID
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ チャンネルが見つかりません")

# メッセージを受け取ったときに呼ばれる処理
@client.event
async def on_message(message):
    if message.author.bot:
        return  # 他のBotのメッセージは無視する

    owner_id = 1150048383524941826  # ボットのオーナー（完全権限）
    admin_ids = [1150048383524941826, 1095693259403173949] # 管理者ID
    moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412, 1138810816905367633]  # モデレーターのIDをここに追加
    vip_ids = [1150048383524941826]  # ←VIPユーザーのIDを追加
    notify_channel_id = 1371322394719031396  # ログチャンネルのID
    react_channel_id = 1125349326269452309  # 👍リアクションを付けるチャンネルのID

    # 特定のチャンネルでメッセージに👍リアクションを付ける
    if message.channel.id == react_channel_id:
        try:
            await message.add_reaction("👍")
        except Exception as e:
            print(f"リアクション失敗: {e}")

    # t!shutdown コマンド（Botを終了）
    if message.content.startswith('t!shutdown'):
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # t!restart コマンド（Botを再起動）
    if message.content.startswith('t!restart'):
        if message.author.id == owner_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("再起動をしました")
            await client.close()
        else:
            await message.channel.send("🛑 オーナー専用コマンドです。")
        return

    # サーバー上で t!tokumei が使われたときの注意メッセージ
    if (
        not isinstance(message.channel, discord.DMChannel)
        and message.content.startswith("t!tokumei")
        and not message.author.bot
    ):
        await message.channel.send("📬 このコマンドはDMで使ってください！\n例：Botに `t!tokumei 明日テストいやだ` と送ると、匿名で投稿されます。")
        return


    # 雑談の自動返信（コマンドじゃないメッセージだけ）
    if not message.content.startswith("t!") and message.content.strip():
        text = message.content.lower()

        if "おはよ" in text:
            responses = [
                'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
                '学校行けよ',
                '寝坊してない？( ˘⁠ω˘ )',
                '早起き過ぎ！？！？！？！',
                'おっそ',
            ]
            await message.channel.send(random.choice(responses))

        elif "おやすみ" in text:
            responses = [
                'おやすみ',
                'いい夢見てね！',
                '今日もnukeされずに済んだね！',
                'おやすみのnukeは？',
                'おつかれさま、ゆっくり休んでね〜',
                'おやすみ〜',
                'もう起きてこなくていいよ',
            ]
            await message.channel.send(random.choice(responses))

    # 存在しないコマンドに反応する処理
    if message.content.startswith("t!"):
        known_prefixes = [
            't!help',        # ヘルプ表示
            't!say',         # 指定チャンネルにメッセージ送信
            't!shutdown',    # Bot終了（owner限定）
            't!restart',     # Bot再起動（owner限定）
            't!omikuji',     # おみくじ（1日1回制限あり）
            't!yamu',        # 病み構文連投（管理者限定）
            't!ai',          # なんちゃってAI返信
            't!user',        # ユーザー情報表示
            't!stats',       # 使用状況表示
            't!mittyan',     # みっちゃん生存確認（自動通知）
            't!serverinfo',  # サーバー情報表示
            't!admin',       # 管理者向けの設定確認
            't!dm',          # ユーザーへのDM送信（管理者限定）
            't!chatgpt',     # OpenAIにメッセージを送る（簡易AI）
            't!tokumei',     # 匿名投稿（Webhook）
            't!avatar',      # ユーザーのアイコン表示
            't!ping'         # 応答速度を表示
        ]

        # "t!" だけのメッセージは無視
        if message.content.strip() == "t!":
            return

        # 一致する既存コマンドがなければ警告
        if not any(message.content.startswith(cmd) for cmd in known_prefixes):
            await message.channel.send("❌ そんなコマンドはありません。[t!help]で確認してください。")

    await client.process_commands(message)

# Cog 読み込み：setup_hookを使う方法（推奨）
@client.event
async def setup_hook():
    await client.load_extension("cogs.ping")  # ping.py を読み込む
    await client.load_extension("cogs.say")   # ← say.pyを読み込む
    await client.load_extension("cogs.dm")  # ← dm.py を読み込む
    await client.load_extension("cogs.tokumei")  # tokumei.py を読み込む
    await client.load_extension("cogs.ai") # ai.pyを読み込む
    await client.load_extension("cogs.user")  # user.pyを読み込む
    await client.load_extension("cogs.admin") # admin.pyを読み込む
    await client.load_extension("cogs.yamu") # yamu.pyを読み込む
    await client.load_extension("cogs.serverinfo") # serverinfo.pyを読み込む
    await client.load_extension("cogs.stats")  # stats.py を読み込む
    await client.load_extension("cogs.chatgpt") # chatgpt.pyを読み込む
    await client.load_extension("cogs.mittyan") # mittyan.pyを読み込む
    await client.load_extension("cogs.omikuji") # omikuji.pyを読み込む
    await client.load_extension("cogs.help")  # ← help.pyを読み込む

# トークン未設定チェック
if not TOKEN:
    print("❌ エラー: DISCORD_TOKEN が設定されていません。")
    exit()

# Botの起動
client.run(TOKEN)
