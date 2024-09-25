import discord
from discord import app_commands as ac

import ollama

cootshk_user_id = 921605971577548820

client = discord.Client(intents=discord.Intents.all())
tree = ac.CommandTree(client)

@tree.command(name="test", description="Test command")
@ac.allowed_installs(guilds=True, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def test(ctx: discord.Interaction):
    await ctx.response.send_message("Test command, from a user-installed bot!",ephemeral=True)

@tree.command(name="sync", description="Sync the commands")
@ac.allowed_installs(guilds=True, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def sync(ctx: discord.Interaction):
    if ctx.user.id != cootshk_user_id:
        await ctx.response.send_message("nice try lol", ephemeral=True)
        return
    await tree.sync()
    await ctx.response.send_message("Synced the commands!", ephemeral=True)

@tree.command(name="ping", description="Ping the bot")
@ac.allowed_installs(guilds=True, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message(f"Pong!")

try:
    with open(".env", "r") as f:
        token = f.read()
except FileNotFoundError:
    token = input("Enter your bot token: ")
    with open(".env", "w") as f:
        f.write(token)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await tree.sync()
client.run(token)