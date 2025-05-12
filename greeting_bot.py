import discord
import os
import random  # ランダム返信のために必要！

# トークンを環境変数から読み取る
TOKEN = os.getenv("DISCORD_TOKEN")

# メッセージを読むための設定
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました：{client.user}')

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content == 'おはよう':
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

    elif message.content == 'おやすみ':
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
