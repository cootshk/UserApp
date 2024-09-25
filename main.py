import discord
from discord import app_commands as ac

from ollama import AsyncClient

cootshk_user_id = 921605971577548820
kenbot_user_id = 736280726957326537

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
    print("Syncing...")
    await tree.sync()
    await ctx.response.send_message("Synced the commands!", ephemeral=True)

@tree.command(name="ping", description="Ping the bot")
@ac.allowed_installs(guilds=True, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ping(ctx: discord.Interaction):
    await ctx.response.send_message(f"Pong!")

@tree.command(name="insult", description="Insult someone")
@ac.allowed_installs(guilds=False, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=False)
async def insult(ctx: discord.Interaction, user: discord.User):
    if user.id == cootshk_user_id:
        await ctx.response.send_message("nah, i don't think so", ephemeral=True)
        return
    if user.id == client.user.id or user.id == kenbot_user_id:
        # Insult the user instead
        self_insult = True
        user = ctx.user
    else:
        self_insult = False
    # last_messages = []
    # async for msg in ctx.channel.history(limit=500, oldest_first=False):
    #     if msg.author.id == user.id:
    #         last_messages += [msg.content]
    await ctx.response.send_message(f"Insulting...\n\nI can't see messages because discord is dumb.", ephemeral=False)
    # print(last_messages)
    try: 
        member = ctx.guild.get_member(user.id)
    except:
        member = None
    prompt = (f"Please insult the following discord user: {user.name}. "
             +f"Their display name is \"{user.display_name}\". "
             +f"This user made their account on: {user.created_at}. "
             +f"This user has the following ID: {user.id}. "
             +f"Here are the user's flags: {user.public_flags.all()} "
             +f"{f'This user is using this avatar decoration: {user.avatar_decoration_sku_id}.' if user.avatar_decoration is not None else ''} "
             +f"This user is a {'bot' if user.bot else 'human'}. "
             +f"{'This user is a verified bot.' if user.public_flags.verified_bot or user.public_flags.system else ''} "
             +f"{f'This user has been paying for Nitro since {member.premium_since}.' if member is not None and member.premium_since else ''} "
            #  +f"Their last 50 messages are: {last_messages}"
             +f"{'This user tried to insult you. Please insult them instead. ' if self_insult else f'You were asked to insult this user by {ctx.user.display_name}. '}",
             )[0]
    print(prompt)
    response = await AsyncClient().chat(model="mistral", messages=[{'role': 'user', 'content': prompt}])
    print("Got response", response)
    await ctx.followup.send(response["message"]["content"],)# username=ctx.user.nick, avatar_url=ctx.user.guild_avatar.url)

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
    # await tree.sync()
client.run(token)