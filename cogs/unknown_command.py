import discord
from discord.ext import commands

class UnknownCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.known_prefixes = [
            't!help', 't!say', 't!shutdown', 't!restart', 't!omikuji',
            't!yamu', 't!ai', 't!user', 't!stats', 't!mittyan', 't!serverinfo',
            't!admin', 't!dm', 't!chatgpt', 't!tokumei', 't!avatar', 't!ping'
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.content.startswith("t!"):
            if message.content.strip() == "t!":
                return
            if not any(message.content.startswith(cmd) for cmd in self.known_prefixes):
                await message.channel.send("❌ そんなコマンドはありません。[t!help]で確認してください。")

async def setup(bot):
    await bot.add_cog(UnknownCommand(bot))
