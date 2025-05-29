import discord
from discord.ext import commands

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo_command(self, ctx):
        """サーバー情報を表示します（モデレーター以上限定）"""
        moderator_ids = [
            1150048383524941826,  # オーナー
            1095693259403173949,  # 管理者
            1354645428095680563,  # モデレーター
            841603812548411412,
            1138810816905367633
        ]
        notify_channel_id = 1371322394719031396  # ログ送信用

        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        guild = ctx.guild
        owner_user = guild.owner
        total_members = guild.member_count
        bot_count = len([member for member in guild.members if member.bot])
        human_count = total_members - bot_count
        created_at = guild.created_at.strftime('%Y-%m-%d %H:%M:%S')
        bot_joined_at = guild.me.joined_at.strftime('%Y-%m-%d %H:%M:%S')
        bot_owner_id = 1150048383524941826
        is_owner_in_server = guild.get_member(bot_owner_id) is not None

        embed = discord.Embed(
            title=f"📊 サーバー情報：{guild.name}",
            color=discord.Color.teal()
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="サーバー名", value=guild.name, inline=False)
        embed.add_field(name="サーバーID", value=str(guild.id), inline=False)
        embed.add_field(name="総参加人数", value=f"{total_members}人", inline=True)
        embed.add_field(name="ユーザー数", value=f"{human_count}人", inline=True)
        embed.add_field(name="Bot数", value=f"{bot_count}体", inline=True)
        embed.add_field(name="サーバー作成日", value=created_at, inline=False)
        embed.add_field(name="サーバーオーナー", value=owner_user.name, inline=False)
        embed.add_field(name="みっちゃんBot導入日", value=bot_joined_at, inline=False)
        embed.add_field(name="オーナー参加中？", value="✅ はい" if is_owner_in_server else "❌ いいえ", inline=False)

        await ctx.send(embed=embed)

        # ログ送信
        log_channel = self.bot.get_channel(notify_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
