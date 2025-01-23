import discord
from discord.ext import commands
import random
import string
from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='.', intents=intents)

# Dictionary to store generated keys and premium statuses
keys = {}
premium_users = {}

# Command to setup key generation channels
@bot.command()
@commands.has_permissions(administrator=True)
async def setup(ctx):
    await ctx.send("What channels would you like keys generated in? Please mention the channel(s).")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=60.0)
        channels = msg.channel_mentions
        if not channels:
            await ctx.send("No channels mentioned. Please mention at least one channel.")
            return
        for channel in channels:
            keys[channel.id] = []
        await ctx.send(f"Channels set for key generation: {', '.join([channel.mention for channel in channels])}")
    except TimeoutError:
        await ctx.send("Setup timed out. Please try again.")

# Command to generate keys
@bot.command()
@commands.has_permissions(administrator=True)
async def generate_key(ctx, amount: int):
    if ctx.channel.id not in keys:
        await ctx.send("This channel is not set for key generation. Please use /setup first.")
        return
    generated_keys = []
    for _ in range(amount):
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        generated_keys.append(key)
        keys[ctx.channel.id].append(key)
    await ctx.send(f"Generated keys: {', '.join(generated_keys)}")

# Command to give premium status
@bot.command()
@commands.has_permissions(administrator=True)
async def P(ctx, member: discord.Member, duration: str = None):
    premium_users[member.id] = 'premium'
    await ctx.send(f"{member.mention} has been given premium status.")

@bot.command()
@commands.has_permissions(administrator=True)
async def P_plus(ctx, member: discord.Member, duration: str = None):
    premium_users[member.id] = 'premium+'
    await ctx.send(f"{member.mention} has been given premium+ status.")

# Command to check the bot's response time
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

# Command to check who invited the user and their invites
@bot.command()
async def Inv_Req(ctx):
    # Implement logic to track invites and return information
    await ctx.send("This feature is under development.")

# Command to claim a key
@bot.command()
async def Key_Claim(ctx, key: str):
    for channel_id, channel_keys in keys.items():
        if key in channel_keys:
            keys[channel_id].remove(key)
            await ctx.send(f"Key {key} claimed successfully!")
            return
    await ctx.send("Invalid key.")

# Command to generate free code keys
@bot.command()
@commands.has_permissions(administrator=True)
async def Code_Key_Gen(ctx, amount: int):
    generated_keys = []
    for _ in range(amount):
        key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        generated_keys.append(key)
    await ctx.send(f"Generated free code keys: {', '.join(generated_keys)}")

# Run the bot with your token
bot.run(MTMzMTg1ODg2Nzg4NTE3ODk0MA.GuxwUY.s8cMQadmJ1lzax7dHUA5WdgMf3NWzDPkXJ3rqA)
