# ✅ 必要なライブラリをインポート
import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ✅ on_member_join：メンバー参加時に発火するイベント
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # ✅ たまごのお部屋以外では何もしない（サーバーIDチェック）
        if member.guild.id != 1122825314377138217:
            return

        try:
            # ✅ 送信するDMの内容（改行含む）
            message = (
                f"ようこそ **たまごのお部屋** へ！\n\n"
                f"📌 まずはこちらをご確認ください：\n"
                f"👉 https://discord.com/channels/1122825314377138217/1125349311669076038 （ルール）\n"
                f"📨 招待リンク: https://discord.gg/7RcSkytKDq\n\n"
                f"みんなで楽しく雑談しましょう！🧊"
            )

            # ✅ DM送信（エラーが出ることもあるのでtry）
            await member.send(message)

        except discord.Forbidden:
            # ✅ DMが拒否されていた場合はスルー
            print(f"[WELCOME] {member} にDMを送れませんでした（DM拒否）")
        except Exception as e:
            print(f"[WELCOME] DM送信エラー: {e}")

# ✅ Cog登録
async def setup(bot):
    await bot.add_cog(Welcome(bot))
