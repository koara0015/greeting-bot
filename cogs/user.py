import discord
from discord.ext import commands

class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="user")
    async def user_command(self, ctx, arg=None):
        """ユーザー情報を表示（管理者・モデレーター限定）"""
        moderator_ids = [
            1150048383524941826,  # オーナー
            1095693259403173949,  # 管理者
            1354645428095680563,  # モデレーター
            841603812548411412,
            1138810816905367633
        ]
        notify_channel_id = 1371322394719031396

        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        target_user = ctx.author
        target_member = ctx.guild.get_member(ctx.author.id)

        # 引数がある場合は指定されたユーザー
        if arg:
            if arg.startswith("<@") and arg.endswith(">"):
                arg = arg.replace("<@", "").replace("!", "").replace(">", "")
            try:
                user_id = int(arg)
                target_user = await self.bot.fetch_user(user_id)
                target_member = ctx.guild.get_member(user_id)
            except:
                await ctx.send("⚠️ ユーザーが見つかりませんでした。")
                return

        embed = discord.Embed(
            title=f"🧑‍💼 ユーザー情報：{target_user.name}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else target_user.default_avatar.url)
        embed.add_field(name="ユーザー名", value=target_user.name, inline=False)
        embed.add_field(name="ユーザーID", value=target_user.id, inline=False)
        embed.add_field(name="アカウント作成日", value=target_user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

        joined_date = "不明"
        if target_member and target_member.joined_at:
            joined_date = target_member.joined_at.strftime('%Y-%m-%d %H:%M:%S')

        embed.add_field(name="サーバー参加日", value=joined_date, inline=False)

        await ctx.send(embed=embed)

        # ログ送信
        log_channel = self.bot.get_channel(notify_channel_id)
        if log_channel:
            await log_channel.send(embed=embed)

    # t!avatarコマンド

    @commands.command(name="avatar")
    async def avatar_command(self, ctx, arg=None):
        """ユーザーのアバターを表示（誰でも可）"""
        target_user = ctx.author

        if arg:
            if arg.startswith("<@") and arg.endswith(">"):
                arg = arg.replace("<@", "").replace("!", "").replace(">", "")
            try:
                user_id = int(arg)
                target_user = await self.bot.fetch_user(user_id)
            except:
                await ctx.send("⚠️ ユーザーが見つかりませんでした。")
                return

        avatar_url = target_user.avatar.url if target_user.avatar else target_user.default_avatar.url
        embed = discord.Embed(
            title=f"{target_user.name} のアバター",
            color=discord.Color.blurple()
        )
        embed.set_image(url=avatar_url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(User(bot))
