import discord
from discord.ext import commands
from datetime import datetime
import random

class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.omikuji_usage = {}  # ユーザーID: 最後の使用日

    @commands.command(name="omikuji")
    async def omikuji(self, ctx):
        today = datetime.now().date()
        user_id = ctx.author.id
        last_used = self.omikuji_usage.get(user_id)

        if last_used == today:
            await ctx.send("おみくじは1日1回限定です。")
            return

        self.omikuji_usage[user_id] = today

        fortunes = {
            "特大凶": ["地獄の始まり。今日の運勢は0です", "逆にレアだと思えば……？", "もう寝よう！"],
            "大凶": ["今日はなにもかもが裏目に出る日…", "一歩踏み出す前に3回深呼吸して", "今日はおとなしくしていよう"],
            "凶": ["なんかうまくいかない気がする…", "でも気をつけてれば大丈夫！たぶん！", "まあ、凶ならまだマシよ"],
            "末吉": ["ちょっと運がある。ちょっとだけ", "結果は努力次第！", "タイミングを見極めよう"],
            "小吉": ["小さな幸せに気づける日", "いいこともある。たぶん", "今日は地味に良い日！"],
            "中吉": ["なかなかいい感じの運勢！", "落ち着いて行動すれば吉", "流れに乗れ！"],
            "吉": ["いいことありそう！", "ラッキーアイテムはチョコ", "ちょっと自信を持ってみよう！"],
            "大吉": ["最高の一日になる！", "思い切って行動してみよう！", "やるなら今！"],
            "たまご": ["今日はたまごの言うことを聞いといたらうまくいく！", "今日は過去最高潮に運がいい！", "何でも挑戦すれば全ていい方向に行く！"]
        }

        choices = ["吉", "小吉", "末吉", "中吉", "凶", "大吉", "大凶", "特大凶", "たまご"]
        weights = [18, 19, 19, 19, 15, 4, 4, 2, 1]  # 合計 = 101

        result = random.choices(choices, weights=weights, k=1)[0]
        comment = random.choice(fortunes[result])

        await ctx.send(f"🎴 おみくじの結果：**{result}**！\n{comment}")

async def setup(bot):
    await bot.add_cog(Omikuji(bot))
