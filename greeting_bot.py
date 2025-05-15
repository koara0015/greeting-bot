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

    owner_id = 1150048383524941826  # ボットのオーナー（完全権限）
    admin_ids = [1150048383524941826, 1095693259403173949] # 管理者ID
    moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563]  # モデレーターのIDをここに追加
    notify_channel_id = 1371322394719031396  # ログチャンネルのID
    react_channel_id = 1125349326269452309  # 👍リアクションを付けるチャンネルのID
    start_time = datetime.now()  # 起動時間を記録

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
        
    # t!say コマンド（Botが指定チャンネルに発言）
    if message.content.startswith('t!say'):
        if message.author.id in moderator_ids:
            parts = message.content.split(' ', 2)
            if len(parts) < 3:
                await message.channel.send("使い方：t!say [チャンネルID or #チャンネル] [メッセージ]")
                return

            # メッセージと送信先チャンネルの取得
            target_channel = None

            # ① チャンネルメンションの場合
            if message.channel_mentions:
                target_channel = message.channel_mentions[0]

            # ② 数字でチャンネルIDを指定した場合
            else:
                try:
                    channel_id = int(parts[1])
                    target_channel = client.get_channel(channel_id)
                except:
                    await message.channel.send("⚠️ チャンネルIDの形式が正しくありません。")
                    return

            if not target_channel:
                await message.channel.send("⚠️ チャンネルが見つかりませんでした")
                return

            # ③ リンクが含まれていたら却下
            if "http://" in parts[2] or "https://" in parts[2] or "www." in parts[2] or "discord.gg" in parts[2]:
                await message.channel.send("⚠️ リンクが含まれているため却下しました。")
                log_channel = client.get_channel(notify_channel_id)
                if log_channel:
                    await log_channel.send(f"⚠️ {message.author.display_name} によるリンク投稿を却下しました：{parts[2]}")
                return

            try:
                await target_channel.send(parts[2])
                await message.channel.send("✅ メッセージを送信しました")
            except Exception as e:
                await message.channel.send(f"⚠️ エラーが発生しました: {e}")
        else:
            await message.channel.send("⚠️ モデレーター以上の権限が必要です。")
        return

    # t!help コマンド（コマンド一覧を表示）
    if message.content == 't!help':
        if message.author.id in moderator_ids:
            embed = discord.Embed(
                title="🤖 コマンド一覧",
                description="このBotで使えるコマンド一覧です！",
                color=discord.Color.green()
            )
            embed.add_field(name="🟢 t!help", value="コマンド一覧を表示します（モデレーター以上限定）", inline=False)
            embed.add_field(name="🟢 t!say [チャンネルID] [メッセージ]", value="このボットに指定した言葉を言わせます（モデレーター以上限定）", inline=False)
            embed.add_field(name="🟢 t!shutdown", value="Botを終了します（オーナー限定）", inline=False)
            embed.add_field(name="🟢 t!restart", value="Botを再起動します（オーナー限定）", inline=False)
            embed.add_field(name="🟢 t!omikuji", value="1日1回限定のおみくじをやります（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!yamu [チャンネルID]", value="みっちゃんが過去に打った病み構文を一気に流します（モデレーター以上限定）", inline=False)
            embed.add_field(name="🟢 t!ai [質問]", value="aiが質問に対して適当に返してくれます（誰でも可）", inline=False)
            embed.add_field(name="🟢 t!user [ユーザーID]", value="ユーザー情報を表示してくれます（モデレーター以上限定）", inline=False)
            embed.add_field(name="🔴 t!chatgpt [質問]", value="現在使用不可", inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("⚠️ モデレーター以上の権限が必要です。")
        return
            
    # t!stats コマンド（Botの統計情報）
    if message.content == 't!stats':
        uptime = datetime.now() - start_time
        uptime_str = str(uptime).split('.')[0]  # 小数点以下カット

        guild_count = len(client.guilds)
        user_count = len(set(member.id for guild in client.guilds for member in guild.members))

        embed = discord.Embed(
            title="📊 Botの統計情報",
            color=discord.Color.teal()
        )
        embed.add_field(name="⏱️ 起動時間", value=uptime_str, inline=False)
        embed.add_field(name="🧭 サーバー数", value=str(guild_count), inline=True)
        embed.add_field(name="👥 ユーザー数", value=str(user_count), inline=True)

        await message.channel.send(embed=embed)
        return

        # t!chatgpt コマンド（API制限メッセージ）
    if message.content.startswith("t!chatgpt"):
        await message.channel.send("🔴 API制限に達したため利用不可です。")
        return

    # t!user コマンド（ユーザー情報を表示・管理者限定）
    if message.content.startswith('t!user'):
        if message.author.id in moderator_ids:
            parts = message.content.split()
            target_user = message.author
            target_member = message.guild.get_member(target_user.id)

            # 引数が指定されている場合（ID または メンション対応）
            if len(parts) == 2:
                arg = parts[1]

                # メンション形式（<@1234567890> または <@!1234567890>）をIDに変換
                if arg.startswith("<@") and arg.endswith(">"):
                    arg = arg.replace("<@", "").replace("!", "").replace(">", "")

                try:
                    user_id = int(arg)
                    target_user = await client.fetch_user(user_id)
                    target_member = message.guild.get_member(user_id)
                except:
                    await message.channel.send("⚠️ ユーザーが見つかりませんでした。")
                    return

            # 埋め込みメッセージを作成
            embed = discord.Embed(
                title=f"🧑‍💼 ユーザー情報：{target_user.name}",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else target_user.default_avatar.url)
            embed.add_field(name="ユーザー名", value=target_user.name, inline=False)
            embed.add_field(name="ユーザーID", value=target_user.id, inline=False)
            embed.add_field(name="アカウント作成日", value=target_user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
            embed.add_field(
                name="サーバー参加日",
                value=target_member.joined_at.strftime('%Y-%m-%d %H:%M:%S') if target_member and target_member.joined_at else "不明",
                inline=False
            )

            await message.channel.send(embed=embed)
        else:
            await message.channel.send("⚠️ モデレーター以上の権限が必要です。")
        return


    # t!yamu コマンド（病み構文を一気に投稿・クールダウンあり）
    if message.content.startswith('t!yamu'):
        if message.author.id in moderator_ids:
            # クールダウンチェック
            now = datetime.now()
            cooldown_time = 15 * 60  # 15分（秒）
            user_id = message.author.id
            last_used = omikuji_usage.get(f"yamu_{user_id}")

            if last_used:
                elapsed = (now - last_used).total_seconds()
                if elapsed < cooldown_time:
                    minutes = int((cooldown_time - elapsed) // 60)
                    seconds = int((cooldown_time - elapsed) % 60)
                    await message.channel.send(f"⚠️ クールダウン中です。あと {minutes} 分 {seconds} 秒お待ちください。")
                    return

            omikuji_usage[f"yamu_{user_id}"] = now  # 使用時間を記録

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

                for line in lines:
                    await target_channel.send(line)
                    await asyncio.sleep(0.1)

                log_channel = client.get_channel(notify_channel_id)
                if log_channel:
                    await log_channel.send(f"病み構文を『{target_channel.name}』に投稿しました")

            except Exception as e:
                await message.channel.send(f"⚠️ エラーが発生しました: {e}")
        else:
            await message.channel.send("⚠️ モデレーター以上の権限が必要です。")
        return

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

        # ログチャンネルに通知
        log_channel = client.get_channel(notify_channel_id)
        if log_channel:
            await log_channel.send(f"{message.author.display_name} さんがおみくじを実行しました。")
        return

        # t!ai コマンド（なんちゃってAI返信）
    if message.content.startswith('t!ai'):
        prompt = message.content[5:].strip()
        if not prompt:
            await message.channel.send("使い方：t!ai [質問やメッセージ]")
            return

        responses = [
            f"とりあえずDiscordを閉じてから考えたら？",
            f"口臭いからもう話さない方がいいんじゃない？",
            f"下ネタやめてください！セクハラですよ！",
            f"{prompt} ね、僕にはわかるけどお前には教えてやんない",
            f"すみません、よくわかりませんでした。",
            f"自分で考えたら？",
            f"ggrks",
            f"自分で調べたら？",
            f"お母さんにでも聞いたら？",
            f"そもそも誰お前。",
            f"何でそんなに滑舌悪いのに早口で喋ってるの？",
            f"そういう質問はボットに聞くべきじゃないと思う",
            f"下ネタやめてください。",
            f"AIと話してて人生楽しいの？",
            f"まずはDiscordを開きたまごのお部屋というサーバーを開く。その後メンバー達が助けてくれて解決する。",
            f"死ね。",
            f"もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ"
        ]

        await message.channel.send(random.choice(responses))

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

    # みっちゃんのステータス（オンライン・オフライン）を監視するイベント
@client.event
async def on_presence_update(before, after):
    # みっちゃんのユーザーID
    target_user_id = 1018830502288953354
    notify_channel_id = 1371688028652965980

    # 対象がみっちゃん以外なら無視
    if after.id != target_user_id:
        return

    # ステータスが変化したとき
    if before.status != after.status:
        channel = client.get_channel(notify_channel_id)
        if not channel:
            print("通知チャンネルが見つかりませんでした")
            return

        # オンラインになったとき
        if after.status == discord.Status.online:
            await channel.send("🟢みっちゃんがオンラインになりました")
        # オフラインになったとき
        elif after.status == discord.Status.offline:
            await channel.send("🔴みっちゃんがオフラインになりました")

# Botの起動
client.run(TOKEN)
