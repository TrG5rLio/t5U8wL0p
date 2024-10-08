import discord
from discord.ext import commands
import sqlite3
import math
import random

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Connect to SQLite Database (create it if it doesn't exist)
        self.conn = sqlite3.connect('levels.db')
        self.c = self.conn.cursor()

        # Create table if it doesn't exist
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS user_levels (
                guild_id TEXT,
                user_id TEXT,
                level INTEGER,
                xp INTEGER,
                level_up_xp INTEGER,
                PRIMARY KEY (guild_id, user_id)
            )
        ''')
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        guild_id = str(message.guild.id)
        user_id = str(message.author.id)

        # Check if the user exists in the database
        self.c.execute("SELECT * FROM user_levels WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        user = self.c.fetchone()

        if user is None:
            # If the user is not in the database, add them with default values
            self.c.execute("INSERT INTO user_levels (guild_id, user_id, level, xp, level_up_xp) VALUES (?, ?, ?, ?, ?)",
                           (guild_id, user_id, 0, 0, 100))
            self.conn.commit()
            user = (guild_id, user_id, 0, 0, 100)

        cur_level = user[2]
        xp = user[3]
        level_up_xp = user[4]

        # Random XP gain
        xp += random.randint(1, 5)

        # Level up check
        if xp >= level_up_xp:
            cur_level += 1
            xp = 0  # Reset XP after leveling up
            level_up_xp = math.ceil(100 * cur_level ** 2 + 100 * cur_level + 50)

            await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}!")

        # Update user data
        self.c.execute("UPDATE user_levels SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?",
                       (cur_level, xp, level_up_xp, guild_id, user_id))
        self.conn.commit()

    @commands.command(aliases=['lvl', 'level'])
    async def rank(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            member = ctx.author
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        # Retrieve user data from the database
        self.c.execute("SELECT * FROM user_levels WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        user = self.c.fetchone()

        if user is None:
            await ctx.send(f"{member.name} has not earned any XP yet.")
        else:
            level = user[2]
            xp = user[3]
            level_up_xp = user[4]

            await ctx.send(f'''Level Statistics for {member.name}
            \nLevel: {level} \nXP: {xp} \nXP To Level Up: {level_up_xp}''')

async def setup(bot):
    await bot.add_cog(LevelSys(bot))
