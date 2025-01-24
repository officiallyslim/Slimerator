from dotenv import load_dotenv
load_dotenv()
from keep_alive import keep_alive
import discord
from discord import app_commands
from discord.ext import commands
import os
import random

# Enable all intents for the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

# Variables to store channel settings and premium users
welcome_channel = None
leave_channel = None
log_channel = None
premium_users = {}
premium_role = None
command_roles = {}

# Bot Ready Event
@bot.event
async def on_ready():
    await bot.tree.sync()  # Sync slash commands
    print(f'Logged in as {bot.user}')
    print('Slash commands have been synced.')

# Setup command to configure channels
@bot.tree.command(name="setup", description="Set up channels for welcome, leave, or logging.")
@app_commands.describe(option="Choose between welcome, leave, or log", channel="The channel to set")
async def setup(interaction: discord.Interaction, option: str, channel: discord.TextChannel):
    global welcome_channel, leave_channel, log_channel
    if option.lower() == "welcome":
        welcome_channel = channel.id
        await interaction.response.send_message(f"Welcome channel set to {channel.mention}")
    elif option.lower() == "leave":
        leave_channel = channel.id
        await interaction.response.send_message(f"Leave channel set to {channel.mention}")
    elif option.lower() == "log":
        log_channel = channel.id
        await interaction.response.send_message(f"Log channel set to {channel.mention}")
    else:
        await interaction.response.send_message("Invalid option. Use 'welcome', 'leave', or 'log'.")

# Ban command
@bot.tree.command(name="ban", description="Ban a user for a specified duration.")
@app_commands.describe(member="The user to ban", duration="Duration of the ban")
async def ban(interaction: discord.Interaction, member: discord.Member, duration: str):
    await interaction.response.send_message(f"{member.mention} has been banned for {duration}")

# Kick command
@bot.tree.command(name="kick", description="Kick a user from the server.")
@app_commands.describe(member="The user to kick")
async def kick(interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(f"{member.mention} has been kicked")

# Timeout command
@bot.tree.command(name="timeout", description="Timeout a user for a specified duration.")
@app_commands.describe(member="The user to timeout", duration="Duration of the timeout")
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: str):
    await interaction.response.send_message(f"{member.mention} has been timed out for {duration}")

# User Lookup command
@bot.tree.command(name="user_lookup", description="Get information about a user.")
@app_commands.describe(user="The user to look up")
async def user_lookup(interaction: discord.Interaction, user: discord.User):
    embed = discord.Embed(title=f"User Info: {user.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="User ID", value=user.id, inline=True)
    embed.add_field(name="Created At", value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
    await interaction.response.send_message(embed=embed)

# Generate premium access key
@bot.tree.command(name="generate", description="Generate a premium access key.")
async def generate(interaction: discord.Interaction):
    key = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(6, 18)))
    await interaction.response.send_message(f"Your access key: `{key}`", ephemeral=True)

# Premium management commands
@bot.tree.command(name="premium", description="Grant premium access to a user.")
@app_commands.describe(user="The user to grant premium")
async def premium(interaction: discord.Interaction, user: discord.Member):
    premium_users[user.id] = True
    await interaction.response.send_message(f"{user.mention} is now a premium user!")

@bot.tree.command(name="premium_delete", description="Remove premium access from a user.")
@app_commands.describe(user="The user to remove premium from")
async def premium_delete(interaction: discord.Interaction, user: discord.Member):
    premium_users.pop(user.id, None)
    await interaction.response.send_message(f"Premium removed from {user.mention}")

@bot.tree.command(name="premium_role", description="Set the premium role.")
@app_commands.describe(role="The role to assign to premium users")
async def premium_role_command(interaction: discord.Interaction, role: discord.Role):
    global premium_role
    premium_role = role.id
    await interaction.response.send_message(f"Premium role set to {role.name}")

@bot.tree.command(name="premium_list", description="List all premium users.")
async def premium_list(interaction: discord.Interaction):
    if premium_users:
        user_list = "\n".join([f"<@{user_id}>" for user_id in premium_users.keys()])
        await interaction.response.send_message(f"Premium users:\n{user_list}")
    else:
        await interaction.response.send_message("No premium users.")

# Role-linking for commands
@bot.tree.command(name="set", description="Set required role for a command.")
@app_commands.describe(role="The role required", command="The command to set role for")
async def set_command(interaction: discord.Interaction, role: discord.Role, command: str):
    command_roles[command] = role.id
    await interaction.response.send_message(f"Command `{command}` now requires `{role.name}` role.")

# Slash command to list all available commands
@bot.tree.command(name="commands", description="List all available bot commands.")
async def commands_list(interaction: discord.Interaction):
    command_names = [command.name for command in bot.tree.walk_commands()]
    command_list = "\n".join([f"/{cmd}" for cmd in command_names])
    embed = discord.Embed(title="Available Commands", description=command_list, color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

# Keep bot alive (for Replit hosting)
keep_alive()

# Run the bot using the token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_BOT_TOKEN not found. Please set it in the environment variables.")
