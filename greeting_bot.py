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

client = commands.Bot(command_prefix="t!", intents=intents)

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

    
    # t!help コマンド（コマンド一覧を表示）
    if message.content == 't!help':
        if message.author.id in moderator_ids or message.author.guild_permissions.administrator:
            embed = discord.Embed(
                title="🤖 コマンド一覧",
                description="このBotで使えるコマンド一覧です！",
                color=discord.Color.green()
            )
            embed.add_field(name="🟢 t!help", value="コマンド一覧を表示します（サーバー管理者限定）", inline=False)
            embed.add_field(name="🟢 t!shutdown", value="Botを終了します（オーナー限定）", inline=False)
            embed.add_field(name="🟢 t!restart", value="Botを再起動します（オーナー限定）", inline=False)
            embed.add_field(name="🟢 t!say [チャンネルID] [メッセージ]", value="このボットに指定した言葉を言わせます（サーバー管理者限定）", inline=False)
            embed.add_field(name="🟢 t!ping", value="Botの応答速度を表示します（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!omikuji", value="1日1回限定のおみくじをやります（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!yamu [チャンネルID]", value="みっちゃんが過去に打った病み構文を一気に流します（モデレーター以上限定）", inline=False)
            embed.add_field(name="🟢 t!ai [質問]", value="aiが質問に対して適当に返してくれます（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!user [ユーザーID/メンション]", value="ユーザー情報を表示してくれます（サーバー管理者限定）", inline=False)
            embed.add_field(name="🟢 t!stats", value="このボットのステータスを表示します（サーバー管理者限定）", inline=False)
            embed.add_field(name="🟢 t!avatar [メンション or ID]", value="ユーザーのアバター（アイコン）を表示します（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!serverinfo", value="サーバーの詳細を表示します（サーバー管理者限定）", inline=False)
            embed.add_field(name="🟢 t!admin", value="現在のオーナー・管理者・モデレーター・VIPの一覧を表示します（モデレーター以上限定）", inline=False)
            embed.add_field(name="🟢 t!dm [メンバーID/メンション] [メッセージ]", value="メンバーにDMを送ります（ボット管理者限定）", inline=False)
            embed.add_field(name="🟢 t!tokumei [メッセージ]", value="みっちゃん初号機へのDMのみで使用可（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!mittyan", value="❌❌❌❌（VIP限定）", inline=False)
            embed.add_field(name="🔴 t!chatgpt [質問]", value="現在使用不可", inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("⚠️ モデレーター以上の権限が必要です。")
        return

    # サーバー上で t!tokumei が使われたときの注意メッセージ
    if (
        not isinstance(message.channel, discord.DMChannel)
        and message.content.startswith("t!tokumei")
        and not message.author.bot
    ):
        await message.channel.send("📬 このコマンドはDMで使ってください！\n例：Botに `t!tokumei 明日テストいやだ` と送ると、匿名で投稿されます。")
        return

    # t!omikuji コマンド
    if message.content == 't!omikuji':
        today = datetime.now().date()
        user_id = message.author.id
        last_used = omikuji_usage.get(user_id)

        if last_used == today:
            await message.channel.send("おみくじは1日1回限定です。")
            return

        omikuji_usage[user_id] = today

        fortunes = {
            "特大凶": ["地獄の始まり。今日の運勢は0です", "逆にレアだと思えば……？", "もう寝よう！"],
            "大凶":   ["今日はなにもかもが裏目に出る日…", "一歩踏み出す前に3回深呼吸して", "今日はおとなしくしていよう"],
            "凶":     ["なんかうまくいかない気がする…", "でも気をつけてれば大丈夫！たぶん！", "まあ、凶ならまだマシよ"],
            "末吉":   ["ちょっと運がある。ちょっとだけ", "結果は努力次第！", "タイミングを見極めよう"],
            "小吉":   ["小さな幸せに気づける日", "いいこともある。たぶん", "今日は地味に良い日！"],
            "中吉":   ["なかなかいい感じの運勢！", "落ち着いて行動すれば吉", "流れに乗れ！"],
            "吉":     ["いいことありそう！", "ラッキーアイテムはチョコ", "ちょっと自信を持ってみよう！"],
            "大吉":   ["最高の一日になる！", "思い切って行動してみよう！", "やるなら今！"],
            "たまご": ["今日はたまごの言うことを聞いといたらうまくいく！", "今日は過去最高潮に運がいい！", "何でも挑戦すれば全ていい方向に行く！"]
        }

        choices = ["吉", "小吉", "末吉", "中吉", "凶", "大吉", "大凶", "特大凶", "たまご"]
        weights = [18, 19, 19, 19, 15, 4, 4, 2, 1]  # 合計 = 101

        result = random.choices(choices, weights=weights, k=1)[0]
        comment = random.choice(fortunes[result])

        await message.channel.send(f"🎴 おみくじの結果：**{result}**！\n{comment}")


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

# トークン未設定チェック
if not TOKEN:
    print("❌ エラー: DISCORD_TOKEN が設定されていません。")
    exit()

# Botの起動
client.run(TOKEN)
