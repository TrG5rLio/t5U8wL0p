import os
import discord
from discord.ext import commands
import asyncpraw
import random

class OnePieceMemes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id='_DALle32QBsEqPvfs8ZmTQ',
            client_secret=os.environ['REDDIT_SECRET'],
            user_agent='script:RandomMeme:v1.0.0 (by /u/ichibehyo)'
        )

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online.")

    @commands.command(name="meme")
    async def fetch_meme(self, ctx):
        subreddit = await self.reddit.subreddit("MemePiece")
        posts_list = []
        async for post in subreddit.hot(limit=10):
            if not post.over_18 and post.author and any(
                post.url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']
            ):
                author_name = post.author.name if post.author else "Anonymous"
                posts_list.append((post.url, author_name))

        if posts_list:
            random_post = random.choice(posts_list)
            meme_embed = discord.Embed(
                title="Random One Piece Meme",
                description="Yohohohohoho",
                color=discord.Color.random()
            )
            meme_embed.set_author(
                name=f"Meme requested by {ctx.author.name}",
                icon_url=ctx.author.avatar.url if ctx.author.avatar else None
            )
            meme_embed.set_image(url=random_post[0])
            meme_embed.set_footer(
                text=f"Post created by {random_post[1]}"
            )
            await ctx.send(embed=meme_embed)
        else:
            await ctx.send("Couldn't find any memes at the moment!")

    def cog_unload(self):
        print(f"{__name__} has been unloaded.")

async def setup(bot):
    await bot.add_cog(OnePieceMemes(bot))
