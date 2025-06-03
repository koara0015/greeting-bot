import discord
from discord.ext import commands
from datetime import datetime
import random

class Omikuji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.omikuji_usage = {}  # ✅ ユーザーごとの最後の使用日を記録

    @commands.command(name="omikuji")
    async def omikuji(self, ctx):
        """おみくじを1日1回引けるコマンド"""

        # ✅ 「t!omikuji」と完全一致しないメッセージは無視
        if ctx.message.content != "t!omikuji":
            return

        today = datetime.now().date()
        user_id = ctx.author.id
        last_used = self.omikuji_usage.get(user_id)

        # ✅ 同じ日に2回使おうとした場合は警告
        if last_used == today:
            await ctx.send("おみくじは1日1回限定です。")
            return

        # ✅ 今日の日付で記録を更新
        self.omikuji_usage[user_id] = today

        # ✅ 結果とコメントの一覧
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

        # ✅ 結果の抽選（出現確率付き）
        choices = ["吉", "小吉", "末吉", "中吉", "凶", "大吉", "大凶", "特大凶", "たまご"]
        weights = [17, 19, 19, 19, 15, 4, 4, 2, 1]  # 合計 = 100
        result = random.choices(choices, weights=weights, k=1)[0]
        comment = random.choice(fortunes[result])

        # ✅ 結果を送信
        await ctx.send(f"🎴 おみくじの結果：**{result}**！\n{comment}")

# ✅ Cogの登録
async def setup(bot):
    await bot.add_cog(Omikuji(bot))
