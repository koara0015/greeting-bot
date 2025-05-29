import discord
import random
from discord.ext import commands

class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ai")
    async def ai_command(self, ctx):
        prompt = ctx.message.content[4:].strip()  # "t!ai " のあとの部分
        if not prompt:
            await ctx.send("使い方：t!ai [質問やメッセージ]")
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
            f"そういうのはボットに聞くべきじゃないと思う",
            f"下ネタやめてください。",
            f"AIと話してて人生楽しいの？",
            f"まずはDiscordを開きたまごのお部屋というサーバーを開く。その後メンバー達が助けてくれて解決する。",
            f"死ね。",
            f"もう昼だよヽ(`Д´)ﾉﾌﾟﾝﾌﾟﾝ",
            f"（急に話しかけてきたけど誰だこいつ）",
            f"そういうことはたまごに言おうね",
            f"そういうことは管理者に言おうね",
            f"そういうことは友達に言おうね",
            f"ボットに話しかけるってことは友達いないの？",
            f"普通に臭いから話しかけないで。",
            f"お前風呂キャンセル界隈か？インターネット越しに臭うぞ"
        ]

        await ctx.send(random.choice(responses))

async def setup(bot):
    await bot.add_cog(AI(bot))
