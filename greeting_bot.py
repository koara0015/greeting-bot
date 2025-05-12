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

    admin_id = 1150048383524941826
    notify_channel_id = 1371322394719031396

    # ==== 管理者コマンド ====
    if message.content.startswith('!shutdown'):
        if message.author.id == admin_id:
            notify_channel = client.get_channel(notify_channel_id)
            if notify_channel:
                try:
                    await notify_channel.send("シャットダウンしました")
                except Exception as e:
                    print(f"通知送信失敗（shutdown）: {e}")
            await client.close()
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    if message.content.startswith('!restart'):
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

    if message.content.startswith('!say'):
        if message.author.id == admin_id:
            parts = message.content.split(' ', 2)
            if len(parts) < 3:
                await message.channel.send("使い方：!say [チャンネルID] [メッセージ]")
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

    if message.content == '!help':
        if message.author.id == admin_id:
            embed = discord.Embed(
                title="🤖 コマンド一覧",
                description="このBotで使えるコマンド一覧です！",
                color=discord.Color.green()
            )
            embed.add_field(name="🟢 !help", value="コマンド一覧を表示します（管理者限定）", inline=False)
            embed.add_field(name="🟢 !say [チャンネルID] [メッセージ]", value="このボットに指定した言葉を言わせます（管理者限定）", inline=False)
            embed.add_field(name="🟢 !shutdown", value="Botを終了します（管理者限定）", inline=False)
            embed.add_field(name="🟢 !restart", value="Botを再起動します（管理者限定）", inline=False)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send("⚠️ 権限がありません")
        return

    # ==== 一般返信 ====
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
