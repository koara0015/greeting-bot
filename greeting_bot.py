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
        return

    admin_id = 1150048383524941826
    notify_channel_id = 1371322394719031396
    react_channel_id = 1125349326269452309

    if message.channel.id == react_channel_id:
        try:
            await message.add_reaction("👍")
        except Exception as e:
            print(f"リアクション失敗: {e}")

    if message.content.startswith('t!shutdown'):
        if message.author.id == admin_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("シャットダウンしました")
            await client.close()
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    if message.content.startswith('t!restart'):
        if message.author.id == admin_id:
            channel = client.get_channel(notify_channel_id)
            if channel:
                await channel.send("再起動をしました")
            await client.close()
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

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
                    log_channel = client.get_channel(notify_channel_id)
                    if log_channel:
                        await log_channel.send(f"{message.author.display_name} が sayコマンドを使用して「{parts[2]}」を送信しました。")
                else:
                    await message.channel.send("⚠️ チャンネルが見つかりませんでした")
            except Exception as e:
                await message.channel.send(f"⚠️ エラーが発生しました: {e}")
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    if message.content.startswith("t!ai"):
        question = message.content[5:].strip()
        if not question:
            await message.channel.send("🤖 何か質問してくれないと、答えられません！")
            return

        fake_responses = [
            "なるほど、それは非常に興味深いですね……！",
            "うーん、それについては哲学的な問いですね。",
            "あなたの感性はとてもユニークです！",
            "もう少しデータが必要ですね🤔",
            "考えてみましたが、お腹が空いたのでやめました。",
            "GPT-999に相談してみます。",
            "その質問、実は宇宙の真理に触れてます。",
            "……その件についてはノーコメントで。",
            "AIでも恋愛は難しいんです…🥺",
            f"「{question}」についてですが、それはつまり……わかりません！"
        ]

        await message.channel.send(random.choice(fake_responses))

        log_channel = client.get_channel(notify_channel_id)
        if log_channel:
            await log_channel.send(f"{message.author.display_name} が aiコマンドを使用しました。")
        return

    # ※このあとに t!help, t!omikuji, t!yamu などが続く（省略）

client.run(TOKEN)
