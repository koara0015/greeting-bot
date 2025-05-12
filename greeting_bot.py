import discord
import os
import random

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'ログインしました：{client.user}')
    channel_id = 1371322394719031396
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    if channel:
        try:
            await channel.send("起動しました")
        except Exception as e:
            print(f"チャンネルへの送信に失敗しました: {e}")
    else:
        print("⚠️ チャンネルが見つかりません")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    # 管理者ID
    admin_id = 1150048383524941826
    notify_channel_id = 1371322394719031396

    # 管理者専用コマンド
    if message.author.id == admin_id:
        if message.content == '!shutdown':
            notify_channel = client.get_channel(notify_channel_id)
            if notify_channel:
                try:
                    await notify_channel.send("シャットダウンしました")
                except Exception as e:
                    print(f"通知送信失敗（shutdown）: {e}")
            await client.close()
            return

        elif message.content == '!restart':
            notify_channel = client.get_channel(notify_channel_id)
            if notify_channel:
                try:
                    await notify_channel.send("再起動をしました")
                except Exception as e:
                    print(f"通知送信失敗（restart）: {e}")
            await client.close()
            return

    # 「おはよ」に反応
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

    # 「おやすみ」に反応
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
