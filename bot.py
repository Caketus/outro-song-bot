import discord
from discord.ext import commands
import asyncio

# Reading the token from the 'token.txt' file
def get_token_from_file(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip()  # Strip to remove any extra spaces or newlines
    return token

# Specify the path to your token file
token_file = 'secret.txt'

# Store the token in a variable
api_token = get_token_from_file(token_file)

# Define bot command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Make sure the bot can read messages
intents.voice_states = True  # Enable voice state intent to read voice channel members
bot = commands.Bot(command_prefix="!", intents=intents)

# Hardcoded URL for the MP3 file
MP3_URL = "https://www.myinstants.com/media/sounds/outro-song-xenogenesis.mp3"  # Replace with the actual URL of your MP3 file

# Bot token (get it from the Discord Developer Portal)
TOKEN = api_token

# Command to join the voice channel and play the specific song
@bot.command()
async def play(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You're not connected to a voice channel!")
        return

    # Connect to the author's voice channel
    channel = ctx.message.author.voice.channel
    voice_client = await channel.connect()

    # Play the hardcoded MP3 file from the URL
    voice_client.play(discord.FFmpegPCMAudio(MP3_URL))

    # Wait for 16 seconds before disconnecting users
    await asyncio.sleep(16)

    # Disconnect all users from the voice channel
    for member in channel.members:
        if member != bot.user:  # Don't disconnect the bot itself
            await member.move_to(None)

    # Disconnect the bot after disconnecting all users
    await voice_client.disconnect()

# Run the bot
bot.run(TOKEN)
