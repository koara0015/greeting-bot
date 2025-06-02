import discord
from discord.ext import commands

class AdminList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # Botインスタンスを保持

    @commands.command(name="admin")
    async def admin_command(self, ctx):
        """オーナー・管理者・モデレーター・VIPの一覧を表示します"""

        # ✅ コマンドが "t!admin" と完全一致しない場合は無視
        if ctx.message.content != "t!admin":
            return

        # ✅ 各権限IDを Bot インスタンスから取得（main.pyで読み込まれている）
        owner_ids = self.bot.owner_ids
        admin_ids = self.bot.admin_ids
        moderator_ids = self.bot.moderator_ids
        vip_ids = self.bot.vip_ids

        # ✅ 実行者がモデレーター以上 or 管理者権限を持っていなければ拒否
        if ctx.author.id not in moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ ユーザーIDからメンションと名前を取得（見つからない場合は「不明」）
        def format_user(user_id):
            user = ctx.guild.get_member(user_id)
            return f"{user.mention}（{user.name}）" if user else f"不明（{user_id}）"

        # ✅ Owner は1人だけと想定
        owner_display = format_user(owner_ids[0]) if owner_ids else "不明"

        # ✅ Admin・Moderator・VIP一覧を整形
        admin_display = [format_user(uid) for uid in admin_ids if uid not in owner_ids]
        moderator_display = [
            format_user(uid)
            for uid in moderator_ids
            if uid not in admin_ids and uid not in owner_ids
        ]
        vip_display = [format_user(uid) for uid in vip_ids]

        # ✅ 埋め込みメッセージを作成
        embed = discord.Embed(
            title="🛡️ 権限一覧",
            description="現在設定されているオーナー・管理者・モデレーター・VIPの一覧です。",
            color=discord.Color.orange()
        )
        embed.add_field(name="👑 Owner", value=owner_display, inline=False)
        embed.add_field(name="🛠️ Admin", value="\n".join(admin_display) or "なし", inline=False)
        embed.add_field(name="🧑‍💼 Moderator", value="\n".join(moderator_display) or "なし", inline=False)
        embed.add_field(name="⭐ VIP", value="\n".join(vip_display) or "なし", inline=False)

        # ✅ 送信！
        await ctx.send(embed=embed)

# ✅ Cogとして登録
async def setup(bot):
    await bot.add_cog(AdminList(bot))
