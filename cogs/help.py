import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        """コマンド一覧を表示（モデレーター以上限定）"""
        moderator_ids = [
            1150048383524941826,  # オーナー
            1095693259403173949,  # 管理者
            1354645428095680563,  # モデレーター
            841603812548411412,
            1138810816905367633
        ]

        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        embed = discord.Embed(
            title="🤖 コマンド一覧",
            description="このBotで使えるコマンド一覧です！",
            color=discord.Color.green()
        )
        embed.add_field(name="🟢 t!help", value="コマンド一覧を表示します（サーバー管理者限定）", inline=False)
        embed.add_field(name="🟢 t!shutdown", value="Botを終了します（オーナー限定）", inline=False)
        embed.add_field(name="🟢 t!restart", value="Botを再起動します（オーナー限定）", inline=False)
        embed.add_field(name="🟢 t!say [チャンネルID] [メッセージ]", value="Botに指定した言葉を言わせます（サーバー管理者限定）", inline=False)
        embed.add_field(name="🟢 t!ping", value="Botの応答速度を表示します（誰でも可）", inline=False)
        embed.add_field(name="🟢 t!omikuji", value="1日1回限定のおみくじをやります（誰でも可）", inline=False)
        embed.add_field(name="🟢 t!yamu [チャンネルID]", value="みっちゃんが過去に打った病み構文を一気に流します（モデレーター以上限定）", inline=False)
        embed.add_field(name="🟢 t!ai [質問]", value="AIが質問に対して適当に返してくれます（誰でも可）", inline=False)
        embed.add_field(name="🟢 t!user [ユーザーID/メンション]", value="ユーザー情報を表示します（サーバー管理者限定）", inline=False)
        embed.add_field(name="🟢 t!stats", value="このBotのステータスを表示します（サーバー管理者限定）", inline=False)
        embed.add_field(name="🟢 t!avatar [メンション or ID]", value="ユーザーのアイコンを表示します（誰でも可）", inline=False)
        embed.add_field(name="🟢 t!serverinfo", value="サーバーの詳細を表示します（サーバー管理者限定）", inline=False)
        embed.add_field(name="🟢 t!admin", value="オーナー・管理者・モデレーター・VIP一覧を表示（モデレーター以上限定）", inline=False)
        embed.add_field(name="🟢 t!dm [ユーザーID/メンション] [メッセージ]", value="DMを送信します（管理者限定）", inline=False)
        embed.add_field(name="🟢 t!tokumei [メッセージ]", value="BotのDMで匿名投稿します（誰でも可）", inline=False)
        embed.add_field(name="🟢 t!mittyan", value="❌❌❌❌（VIP限定）", inline=False)
        embed.add_field(name="🔴 t!chatgpt [質問]", value="現在使用不可", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
