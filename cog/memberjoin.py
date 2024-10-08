import discord
from discord.ext import commands
import os
import easy_pil
import random

class MemberJoinHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f"{__name__} is online.")

  @commands.Cog.listener()
  async def on_member_join(self, member: discord.Member):
    welcome_channel = member.guild.system_channel
    images = list(os.listdir('./cogs/welcome_images'))
    random_image = random.choice(images)
    bg = easy_pil.Editor(f"./cogs/welcome_images/{random_image}").resize((1920, 1080))
    avatar_image = await easy_pil.load_image_async(str(member.avatar.url))
    avatar = easy_pil.Editor(avatar_image).resize((250, 250)).circle_image()
    font_big = easy_pil.Font.poppins(size=90, variant="bold")
    font_small = easy_pil.Font.poppins(size=60, variant="bold")
    bg.paste(avatar, (835, 340))
    bg.ellipse((835, 340), 250, 250, outline="white", stroke_width=5)
    bg.text(
      (960, 620),
      f"Welcome to {member.guild.name}",
      font=font_big,
      color="white",
      align="center"
    )
    bg.text(
      (960, 740),
      f"{member.name} is member #{member.guild.member_count}!",
      font=font_small,
      color="white",
      align="center"
    )
    img_file = discord.File(fp=bg.image_bytes, filename=random_image)
    await welcome_channel.send(
      f"Welcome {member.mention}! Make sure to watch One Piece"
    )
    await welcome_channel.send(file=img_file)

async def setup(bot):
  await bot.add_cog(MemberJoinHandler(bot))
