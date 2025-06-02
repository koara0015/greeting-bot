import discord
from discord.ext import commands
import json  # ← 追加：IDを外部ファイルから読み込むため

class AdminList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ✅ ids.json からID一覧を読み込み
        with open("ids.json", "r") as f:
            ids = json.load(f)

        self.owner_id = ids["owner_id"]
        self.admin_ids = ids["admin_ids"]
        self.moderator_ids = ids["moderator_ids"]
        self.vip_ids = ids["vip_ids"]

    @commands.command(name="admin")
    async def admin_command(self, ctx):
        """オーナー・管理者・モデレーター・VIPの一覧を表示します"""

        # ✅ コマンドが "t!admin" と完全一致しない場合は無視
        if ctx.message.content != "t!admin":
            return

        # ✅ 実行者がモデレーター以上 or 管理者権限を持っていなければ拒否
        if ctx.author.id not in self.moderator_ids and not ctx.author.guild_permissions.administrator:
            await ctx.send("⚠️ モデレーター以上の権限が必要です。")
            return

        # ✅ ユーザーIDからメンションと名前を取得（ユーザーが見つからない場合は「不明」）
        def format_user(user_id):
            user = ctx.guild.get_member(user_id)
            return f"{user.mention}（{user.name}）" if user else f"不明（{user_id}）"

        # ✅ 各権限リストの整形
        owner_display = format_user(self.owner_id)
        admin_display = [format_user(uid) for uid in self.admin_ids if uid != self.owner_id]
        moderator_display = [
            format_user(uid)
            for uid in self.moderator_ids
            if uid not in self.admin_ids and uid != self.owner_id
        ]
        vip_display = [format_user(uid) for uid in self.vip_ids]

        # ✅ 埋め込みメッセージの作成
        embed = discord.Embed(
            title="🛡️ 権限一覧",
            description="現在設定されているオーナー・管理者・モデレーター・VIPの一覧です。",
            color=discord.Color.orange()
        )
        embed.add_field(name="👑 Owner", value=owner_display, inline=False)
        embed.add_field(name="🛠️ Admin", value="\n".join(admin_display) or "なし", inline=False)
        embed.add_field(name="🧑‍💼 Moderator", value="\n".join(moderator_display) or "なし", inline=False)
        embed.add_field(name="⭐ VIP", value="\n".join(vip_display) or "なし", inline=False)

        # ✅ メッセージ送信
        await ctx.send(embed=embed)

# ✅ Cogとして登録
async def setup(bot):
    await bot.add_cog(AdminList(bot))
