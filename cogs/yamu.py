import discord
from discord.ext import commands
import asyncio
from datetime import datetime

class Yamu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}

    @commands.command(name="yamu")
    async def yamu_command(self, ctx, channel_id: int = None):
        """病み構文を一気に流す（モデレーター限定）"""
        moderator_ids = [
            1150048383524941826,
            1095693259403173949,
            1354645428095680563,
            841603812548411412,
            1138810816905367633
        ]
        notify_channel_id = 1371322394719031396

        if ctx.author.id not in moderator_ids:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        if not channel_id:
            await ctx.send("使い方：t!yamu [チャンネルID]")
            return

        now = datetime.now()
        cooldown_time = 15 * 60  # 15分
        user_id = ctx.author.id
        last_used = self.cooldowns.get(user_id)

        if last_used:
            elapsed = (now - last_used).total_seconds()
            if elapsed < cooldown_time:
                minutes = int((cooldown_time - elapsed) // 60)
                seconds = int((cooldown_time - elapsed) % 60)
                await ctx.send(f"⚠️ クールダウン中です。あと {minutes} 分 {seconds} 秒お待ちください。")
                return

        self.cooldowns[user_id] = now

        try:
            target_channel = self.bot.get_channel(channel_id)
            if not target_channel:
                await ctx.send("⚠️ チャンネルが見つかりませんでした。")
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

            log_channel = self.bot.get_channel(notify_channel_id)
            if log_channel:
                await log_channel.send(f"病み構文を『{target_channel.name}』に投稿しました")

        except Exception as e:
            await ctx.send(f"⚠️ エラーが発生しました: {e}")

async def setup(bot):
    await bot.add_cog(Yamu(bot))
