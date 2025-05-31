# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

# ✅ 存在しないコマンドに対応するCog
class UnknownCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # ✅ 有効なコマンド一覧（完全一致で比較）
        self.known_prefixes = [
            't!help', 't!say', 't!shutdown', 't!restart', 't!omikuji',
            't!yamu', 't!ai', 't!user', 't!stats', 't!mittyan', 't!serverinfo',
            't!admin', 't!dm', 't!chatgpt', 't!tokumei', 't!avatar', 't!ping'
        ]

    # ✅ メッセージ受信時に存在しないコマンドを検出
    @commands.Cog.listener()
    async def on_message(self, message):
        # Botのメッセージは無視
        if message.author.bot:
            return

        # t!から始まるメッセージにのみ対応
        if message.content.startswith("t!"):
            if message.content.strip() == "t!":  # 例: ただの "t!"
                return

            # 完全一致する有効なコマンドが見つからない場合
            if not any(message.content.split()[0] == cmd for cmd in self.known_prefixes):
                await message.channel.send("❌ そんなコマンドはありません。[t!help]で確認してください。")

# ✅ Cogとして読み込むためのセットアップ関数
async def setup(bot):
    await bot.add_cog(UnknownCommand(bot))
