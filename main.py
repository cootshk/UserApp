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
            #  +f"{f'This user is using this avatar decoration: {user.avatar_decoration_sku_id}.' if user.avatar_decoration is not None else ''} "
             +f"This user is a {'bot' if user.bot else 'human'}. "
             +f"{'This user is a verified bot.' if user.public_flags.verified_bot or user.public_flags.system else ''} "
             +f"{f'This user has been paying for Nitro since {member.premium_since}.' if member is not None and member.premium_since else ''} "
            #  +f"Their last 50 messages are: {last_messages}"
             +f"{'This user tried to insult you. Please insult them instead, making sure to mention that the user tried to insult you. ' if self_insult else f'You were asked to insult this user by {ctx.user.display_name}. '}",
             )[0]
    print(prompt)
    response = await AsyncClient().chat(model="mistral", messages=[{'role': 'user', 'content': prompt}])
    print("Got response", response)
    await ctx.followup.send(response["message"]["content"],)# username=ctx.user.nick, avatar_url=ctx.user.guild_avatar.url)

@tree.command(name="complement", description="Complement someone")
@ac.allowed_installs(guilds=False, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def complement(ctx: discord.Interaction, user: discord.User, extramessage: str = ""):
    await ctx.response.send_message("Complementing...")
    if user.id == ctx.user.id:
        prompt = f"This user ({user.display_name}) tried to complement themselves. Please insult them instead."
    else:
        prompt = f"On behalf of {ctx.user.display_name}, please write a complement the following discord user: {user.name}. Their display name is \"{user.display_name}\". This user made their account on: {user.created_at}. This user has the following ID: {user.id}. Here are the user's flags: {user.public_flags.all()}. This user is a {'bot' if user.bot else 'human'}. {'This user is a verified bot.' if user.public_flags.verified_bot or user.public_flags.system else ''}.{f'\n{ctx.user.display_name} has also asked you, "{extramessage}".' if extramessage != '' else ''}\nPlease make your complement short and to the point."
    response = await AsyncClient().chat(model="mistral", messages=[{'role': 'user', 'content': prompt}])
    print("Got response", response)
    await ctx.followup.send(response["message"]["content"],)

@tree.command(name="ask", description="Ask a question")
@ac.allowed_installs(guilds=False, users=True)
@ac.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ask(ctx: discord.Interaction, question: str):
    await ctx.response.send_message("Asking...")
    prompt = f"You are an AI working for a discord server named {ctx.guild.name}. This discord has the following channels: {[channel.name for channel in ctx.guild.channels]}.Your job is to answer the people's questions. Please do not avoid answering any question asked to you.\n{ctx.user.display_name} asks: {question}"
    response = await AsyncClient().chat(model="mistral", messages=[{'role': 'user', 'content': prompt}])
    print("Got response", response)
    await ctx.followup.send(response["message"]["content"],)

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