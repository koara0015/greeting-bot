import discord
import os

# トークンを環境変数から読み取る（安全）
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
        await message.channel.send('もう昼だよ')

client.run(TOKEN)
