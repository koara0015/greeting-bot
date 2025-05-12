# 必要なライブラリをインポート
import discord       # Discordの機能を使うため
import os            # トークンを環境変数から読み取るため
import random        # ランダムで返事を選ぶため
import asyncio       # 時間を待つため（sleep関数など）
from datetime import datetime

# トークンを環境変数から取得（セキュリティのため、コードに直接書かない）
TOKEN = os.getenv("DISCORD_TOKEN")

# Botの設定：メッセージの中身を読めるようにする
intents = discord.Intents.default()
intents.message_content = True

# Bot本体を作成
client = discord.Client(intents=intents)

# おみくじの使用履歴（ユーザーID: 最後の使用日）
omikuji_usage = {}

# Botが起動したときに実行される処理
@client.event
async def on_ready():
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

    admin_id = 1150048383524941826
    notify_channel_id = 1371322394719031396
    react_channel_id = 1125349326269452309

    # 👍リアクション機能
    if message.channel.id == react_channel_id:
        try:
            await message.add_reaction("👍")
        except Exception as e:
            print(f"リアクション失敗: {e}")

    # t!shutdown コマンド（Botを終了）
    if message.content.startswith('t!shutdown'):
        if message.author.id == admin_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            await client.close()
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # t!restart コマンド（Botを再起動）
    if message.content.startswith('t!restart'):
        if message.author.id == admin_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("再起動をしました")
            await client.close()
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # t!say コマンド（Botが指定チャンネルに発言）
    if message.content.startswith('t!say'):
        if message.author.id == admin_id:
            parts = message.content.split(' ', 2)
            if len(parts) < 3:
                await message.channel.send("使い方：t!say [チャンネルID] [メッセージ]")
                return
            try:
                channel_id = int(parts[1])
                target = client.get_channel(channel_id)
                if target:
                    await target.send(parts[2])
                    await message.channel.send("✅ メッセージを送信しました")
                else:
                    await message.channel.send("⚠️ チャンネルが見つかりませんでした")
            except Exception as e:
                await message.channel.send(f"⚠️ エラーが発生しました: {e}")
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # t!help コマンド（コマンド一覧を表示）
    if message.content == 't!help':
        if message.author.id == admin_id:
            embed = discord.Embed(
                title="🤖 コマンド一覧",
                description="このBotで使えるコマンド一覧です！",
                color=discord.Color.green()
            )
            embed.add_field(name="🟢 t!help", value="コマンド一覧を表示します（管理者限定）", inline=False)
            embed.add_field(name="🟢 t!say [チャンネルID] [メッセージ]", value="このボットに指定した言葉を言わせます（管理者限定）", inline=False)
            embed.add_field(name="🟢 t!shutdown", value="Botを終了します（管理者限定）", inline=False)
            embed.add_field(name="🟢 t!restart", value="Botを再起動します（管理者限定）", inline=False)
            embed.add_field(name="🟢 t!omikuji", value="1日1回限定のおみくじをやります（誰でも可）", inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # t!omikuji コマンド（おみくじ）
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
            "大吉":   ["最高の一日になる！", "思い切って行動してみよう！", "やるなら今！"]
        }

        result = random.choice(list(fortunes.keys()))
        comment = random.choice(fortunes[result])

        await message.channel.send(f"🎴 おみくじの結果：**{result}**！\n{comment}")

        # ログチャンネルに通知
        log_channel = client.get_channel(notify_channel_id)
        if log_channel:
            await log_channel.send(f"{message.author.display_name} さんがおみくじを実行しました。")
        return

    # "おはよ" を含むメッセージへの返信
    if 'おはよ' in message.content:
        responses = [
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
            '学校行けよ',
            '寝坊してない？( ˘⁠ω˘ )',
            '早起き過ぎ！？！？！？！',
            'おっそ',
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
        ]
        await message.channel.send(random.choice(responses))

    # "おやすみ" を含むメッセージへの返信
    elif 'おやすみ' in message.content:
        responses = [
            'おやすみ',
            'いい夢見てね！',
            '今日もnukeされずに済んだね！',
            'おやすみのnukeは？',
            'おつかれさま、ゆっくり休んでね〜',
            'おやすみ〜',
            'もう起きてこなくていいよ',
            '進捗達成！「いい夢見てね」'
        ]
        await message.channel.send(random.choice(responses))

# Botの起動
client.run(TOKEN)
