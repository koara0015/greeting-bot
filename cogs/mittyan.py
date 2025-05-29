import discord
from discord.ext import commands

class Mittyan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mittyan")
    async def mittyan_command(self, ctx):
        """みっちゃんnukeチェック（VIP限定）"""
        owner_id = 1150048383524941826
        vip_ids = [1150048383524941826]
        notify_channel_id = 1371322394719031396

        if ctx.author.id in vip_ids:
            await ctx.send("このサーバーでnukeはご利用いただけません")
            log_channel = self.bot.get_channel(notify_channel_id)
            if log_channel:
                await log_channel.send(f"{ctx.author.display_name} が t!mittyan を使用しようとしました。")
        else:
            await ctx.send("🛑 オーナーとVIP専用コマンドです。")

async def setup(bot):
    await bot.add_cog(Mittyan(bot))
