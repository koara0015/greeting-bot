import discord
import os
import random  # ランダム返信のために必要！

# トークンを環境変数から読み取る（安全）
TOKEN = os.getenv("DISCORD_TOKEN")

# メッセージを読むための設定
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました：{client.user}')

    # 起動メッセージを送るチャンネルID
    channel_id = 1371322394719031396

    # Botの準備が整うのを明示的に待つ（安全対策）
    await client.wait_until_ready()

    # チャンネル取得して送信（失敗してもBotが止まらないように保護）
    channel = client.get_channel(channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ チャンネルが見つかりません（Botがサーバーにいないか、権限が足りない可能性があります）")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 「おはよ」を含む文に反応
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

    # 「おやすみ」を含む文に反応
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

client.run(TOKEN)
