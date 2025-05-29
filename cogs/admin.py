import discord
from discord.ext import commands

class AdminList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="admin")
    async def admin_command(self, ctx):
        """オーナー・管理者・モデレーター・VIPの一覧を表示します"""
        owner_id = 1150048383524941826
        admin_ids = [1150048383524941826, 1095693259403173949]
        moderator_ids = [1150048383524941826, 1095693259403173949, 1354645428095680563, 841603812548411412, 1138810816905367633]
        vip_ids = [1150048383524941826]

        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        def format_user(user_id):
            user = ctx.guild.get_member(user_id)
            return f"{user.mention}（{user.name}）" if user else f"不明（{user_id}）"

        owner_display = format_user(owner_id)
        admin_display = [format_user(uid) for uid in admin_ids if uid != owner_id]
        moderator_display = [
            format_user(uid)
            for uid in moderator_ids
            if uid not in admin_ids and uid != owner_id
        ]
        vip_display = [format_user(uid) for uid in vip_ids]

        embed = discord.Embed(
            title="🛡️ 権限一覧",
            description="現在設定されているオーナー・管理者・モデレーター・VIPの一覧です。",
            color=discord.Color.orange()
        )
        embed.add_field(name="👑 Owner", value=owner_display, inline=False)
        embed.add_field(name="🛠️ Admin", value="\n".join(admin_display) or "なし", inline=False)
        embed.add_field(name="🧑‍💼 Moderator", value="\n".join(moderator_display) or "なし", inline=False)
        embed.add_field(name="⭐ VIP", value="\n".join(vip_display) or "なし", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdminList(bot))
