# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands
import asyncio
from datetime import datetime
import json  # ← config.jsonを読み込むために追加

# ✅ Yamuクラス（Cogとして定義）
class Yamu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldowns = {}  # 各ユーザーのクールダウン時間を記録

        # ✅ config.json から通知チャンネルIDを読み込み
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        self.notify_channel_id = config.get("notify_channel_id")

    # ✅ t!yamu コマンドを定義
    @commands.command(name="yamu")
    async def yamu_command(self, ctx, channel_arg: str = None):
        """モデレーター専用：病み構文を連投します"""

        # ✅ モデレーター以上の権限があるかチェック
        if ctx.author.id not in self.bot.moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ 引数（チャンネル指定）が無い場合は使い方を表示
        if not channel_arg:
            await ctx.send("使い方：t!yamu [チャンネルID または メンション]")
            return

        # ✅ メンション形式（<#1234567890>）からIDを抽出
        if channel_arg.startswith("<#") and channel_arg.endswith(">"):
            channel_arg = channel_arg.replace("<#", "").replace(">", "")

        try:
            channel_id = int(channel_arg)
            target_channel = self.bot.get_channel(channel_id)
            if not target_channel:
                await ctx.send("⚠️ チャンネルが見つかりませんでした。")
                return
        except ValueError:
            await ctx.send("⚠️ チャンネルIDが不正です。")
            return

        # ✅ クールダウン（15分）チェック
        now = datetime.now()
        user_id = ctx.author.id
        last_used = self.cooldowns.get(user_id)
        cooldown_time = 15 * 60

        if last_used:
            elapsed = (now - last_used).total_seconds()
            if elapsed < cooldown_time:
                minutes = int((cooldown_time - elapsed) // 60)
                seconds = int((cooldown_time - elapsed) % 60)
                await ctx.send(f"⚠️ クールダウン中です。あと {minutes} 分 {seconds} 秒お待ちください。")
                return

        # ✅ クールダウン記録更新
        self.cooldowns[user_id] = now

        # ✅ 送信する病み構文リスト
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

        # ✅ 一行ずつ送信（0.1秒おき）
        for line in lines:
            await target_channel.send(line)
            await asyncio.sleep(0.1)

        # ✅ 投稿ログを通知チャンネルに送信（config.jsonから取得したチャンネルを使用）
        log_channel = self.bot.get_channel(self.notify_channel_id)
        if log_channel:
            await log_channel.send(f"病み構文を『{target_channel.name}』に投稿しました")

# ✅ Cogとして登録
async def setup(bot):
    await bot.add_cog(Yamu(bot))
