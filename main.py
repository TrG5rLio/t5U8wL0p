import os
import asyncio
import discord
from discord.ext import commands, tasks
from itertools import cycle
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

bot_statuses = cycle(["Online", "Offline", "Idle", "Do Not Disturb", "Invisible"])

@tasks.loop(seconds=60)
async def change_bot_status():
  await bot.change_presence(activity=discord.Game(next(bot_statuses)))

@bot.event
async def on_ready():
  print('Logged in')
  change_bot_status.start()
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)

@bot.command()
async def hello(ctx):
  await ctx.send(f"One Piece is Peak {ctx.author.mention}")

@bot.command(aliases=['gm', 'morning'])
async def goodmorning(ctx):
  await ctx.send(f"Ohayou gozaimasu {ctx.author.mention}")

@bot.command(aliases=['gn', 'night'])
async def goodnight(ctx):
  await ctx.send(f"Oyasuminasai {ctx.author.mention}")

@bot.command()
async def sendembed(ctx):
  embed_msg = discord.Embed(
    title="Title", 
    description="Description", 
    color=discord.Color.random()
  )
  embed_msg.set_thumbnail(url=ctx.author.avatar)
  embed_msg.add_field(name="Name", value="Value", inline=False)
  embed_msg.set_image(url=ctx.guild.icon)
  embed_msg.set_footer(text="Footer", icon_url=ctx.author.avatar)
  await ctx.send(embed=embed_msg)

async def load():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      await bot.load_extension(f'cogs.{filename[:-3]}')
      
async def main():
  await load()
  await bot.start(os.environ['TOKEN'])

keep_alive()
asyncio.run(main())
