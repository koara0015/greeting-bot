# 必要なライブラリをインポート
import discord       # Discordの機能を使うため
import os            # トークンを環境変数から読み取るため
import random        # ランダムで返事を選ぶため
import asyncio       # 時間を待つため（sleep関数など）

# 環境変数からトークンを取得（セキュリティのため、コードに直接書かない）
TOKEN = os.getenv("DISCORD_TOKEN")

# Botの設定：メッセージの中身を読めるようにする
intents = discord.Intents.default()
intents.message_content = True

# Bot本体を作成
client = discord.Client(intents=intents)

# Botが起動したときに実行される処理
@client.event
async def on_ready():
    print(f'ログインしました：{client.user}')
    channel_id = 1371322394719031396  # 通知を送るチャンネルのID
    await client.wait_until_ready()  # 接続が安定するまで待つ
    channel = client.get_channel(channel_id)
    if channel:
        try:
            await channel.send("起動しました")  # 起動メッセージを送信
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ チャンネルが見つかりません")

# メッセージを受け取ったときに呼ばれる処理
@client.event
async def on_message(message):
    if message.author.bot:
        return  # 他のBotのメッセージは無視する

    # あなたのユーザーID（管理者限定機能に使用）
    admin_id = 1150048383524941826

    # 通知用チャンネルID（ログなどを送る場所）
    notify_channel_id = 1371322394719031396

    # 👍リアクションを付けたいチャンネルのID
    react_channel_id = 1125349326269452309

    # そのチャンネルでリアクションを付ける
    if message.channel.id == react_channel_id:
        try:
            await message.add_reaction("👍")
        except Exception as e:
            print(f"リアクション失敗: {e}")

    # 管理者だけが使えるコマンド（シャットダウン）
    if message.content.startswith('t!shutdown'):
        if message.author.id == admin_id:
            notify_channel = client.get_channel(notify_channel_id)
            if notify_channel:
                try:
                    await notify_channel.send("シャットダウンしました")
                except Exception as e:
                    print(f"通知送信失敗（shutdown）: {e}")
            await client.close()  # Botを終了
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # Botを再起動（Railwayなどでは再起動される仕組みが必要）
    if message.content.startswith('t!restart'):
        if message.author.id == admin_id:
            notify_channel = client.get_channel(notify_channel_id)
            if notify_channel:
                try:
                    await notify_channel.send("再起動をしました")
                except Exception as e:
                    print(f"通知送信失敗（restart）: {e}")
            await client.close()
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # 管理者がBotに任意のメッセージを送らせる
    if message.content.startswith('t!say'):
        if message.author.id == admin_id:
            parts = message.content.split(' ', 2)
            if len(parts) < 3:
                await message.channel.send("使い方：t!say [チャンネルID] [メッセージ]")
            else:
                try:
                    channel_id = int(parts[1])
                    target_channel = client.get_channel(channel_id)
                    if target_channel:
                        await target_channel.send(parts[2])
                        await message.channel.send("✅ メッセージを送信しました")
                    else:
                        await message.channel.send("⚠️ チャンネルが見つかりませんでした")
                except Exception as e:
                    await message.channel.send(f"⚠️ エラーが発生しました: {e}")
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # コマンド一覧を表示する埋め込みメッセージ
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
            embed.add_field(name="🟢 t!yamu [チャンネルID]", value="みっちゃんが過去に打った病み構文を一気に流します（管理者限定）", inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # 病み構文を一気に投稿するコマンド
    if message.content.startswith('t!yamu'):
        if message.author.id == admin_id:
            parts = message.content.split(' ')
            if len(parts) != 2:
                await message.channel.send("使い方：t!yamu [チャンネルID]")
                return
            try:
                target_channel_id = int(parts[1])
                target_channel = client.get_channel(target_channel_id)
                if not target_channel:
                    await message.channel.send("⚠️ チャンネルが見つかりませんでした")
                    return

                # 投稿する文章（リスト）
                lines = [
                    "こっちは楽しくディスコードやろうとしてるのに全部それが裏目に出て",
                    "嫌がられたり嫌われたりして",
                    "でも周りの人間は自然に上手くやってて",
                    "どうして僕はみんなが当たり前のようにできることができないんだろうって",
                    "人と上手く話すこともできなければ上手く話を聞くこともできないし",
                    "相手の気持ちもわからなければ自分の気持ちすらよく分からないし",
                    "みんなそういうもんだとか人生そんなもんだよだとか言うけど",
                    "彼らが上手く人間関係を築けて僕が築けない時点でそこには差があって",
                    "孤独でいいという人間に限って友達や家族と仲良く彼女がいて",
                    "性格の悪い人間ほどカリスマ性や明るさで人を集めて",
                    "ゲームの上手さが全てじゃないと言いながらそこそこゲームが上手かったりして",
                    "そんな噓ばっかりを嘘とも思わずに口からでまかせに喋りまくって",
                    "指摘されたら思考停止でキレて後で文句言われて",
                    "僕にはもう人間がわからない",
                    "他人と友人というものが分からない",
                    "人との付き合い方もわからない",
                    "だけど僕も僕を理解してくれる人が欲しい",
                    "僕は人間が大嫌いだけど誰か僕を理解してくれる人がいないと苦しい",
                    "だから皆に好かれるような話し方をしたり行動をしたりしても",
                    "やっぱり普通の人達には勝てないし異常者は死んでも異常者なんだよ",
                    "僕が一体何をしたんだよ",
                    "前世でとても悪いことでもしたのか？",
                    "もう僕は何がなんだかわからないしもう何もする気が起きない",
                    "唯一見つけた居場所も僕のせいで崩壊したり僕がその時の感情に任せて発した一言で追い出されたりして",
                    "まだ10数年しか経ってないけどもう人生疲れた",
                    "どうせ今一緒に遊んでくれてる人達とか昔荒らし界隈で僕と荒らしてた人達も心の中ではキモいとかさっさといなくなればいいとか思ってるだろうし",
                    "普通に振舞ってても異常者だし",
                    "異常に振舞っても異常だし",
                    "死にたいけど死にたくない",
                    "僕はもうどうしていいのかわからない"
                ]

                # 一行ずつ送信、0.1秒間隔
                for line in lines:
                    await target_channel.send(line)
                    await asyncio.sleep(0.1)

                # 投稿完了後に通知用チャンネルへ報告
                log_channel = client.get_channel(notify_channel_id)
                if log_channel:
                    try:
                        await log_channel.send(f"病み構文を『{target_channel.name}』に投稿しました")
                    except Exception as e:
                        print(f"報告送信失敗: {e}")

            except Exception as e:
                await message.channel.send(f"⚠️ エラーが発生しました: {e}")
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # おはよ系メッセージに反応
    if 'おはよ' in message.content:
        responses = [
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
            '学校行けよ',
            '寝坊してない？( ˘ω˘ )',
            '早起き過ぎ！？！？！？！',
            'おっそ',
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
            'もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ',
        ]
        await message.channel.send(random.choice(responses))

    # おやすみ系メッセージに反応
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
