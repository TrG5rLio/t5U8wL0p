import discord
from discord.ext import commands
from replit import db
import math
import random

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        # Unique key for each user in the guild
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        key = f"{guild_id}-{user_id}"

        # Check if user is in the database
        if key not in db:
            db[key] = {
                "level": 0,
                "xp": 0,
                "level_up_xp": 100
            }

        user_data = db[key]
        cur_level = user_data["level"]
        xp = user_data["xp"]
        level_up_xp = user_data["level_up_xp"]

        # Random XP gain
        xp += random.randint(1, 5)

        # Level up check
        if xp >= level_up_xp:
            cur_level += 1
            xp = 0  # Reset XP after leveling up
            level_up_xp = math.ceil(100 * cur_level ** 2 + 100 * cur_level + 50)

            await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}!")

        # Update user data
        db[key] = {
            "level": cur_level,
            "xp": xp,
            "level_up_xp": level_up_xp
        }

    @commands.command(aliases=['lvl', 'level'])
    async def rank(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        member_id = str(member.id)
        guild_id = str(ctx.guild.id)
        key = f"{guild_id}-{member_id}"

        if key not in db:
            await ctx.send(f"{member.name} has not earned any xp yet.")
        else:
            user_data = db[key]
            level = user_data["level"]
            xp = user_data["xp"]
            level_up_xp = user_data["level_up_xp"]

            await ctx.send(f'''Level Statistics for {member.name}
            \nLevel: {level} \nXP: {xp} \nXP To Level Up: {level_up_xp}''')

async def setup(bot):
    await bot.add_cog(LevelSys(bot))
