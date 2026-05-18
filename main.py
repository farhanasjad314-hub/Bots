import discord
from discord.ext import commands
import asyncio
from flask import Flask
from threading import Thread

# Render ke liye background server
app = Flask('')

@app.route('/')
def home():
    return "Bots are running 24/7 without ID!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# ----------------- BOTS SETUP -----------------

# YAHA APNE DONO BOTS KE TOKENS DAALEIN
BOT_TOKEN_1 = "MTUwNTg0MjU5NDM3MzA0NjMxMw.GOCgpD.Q0zP0wA6_rBC0fpHUit-31kd31WKOJ4zbyOxQ0"
BOT_TOKEN_2 = "MTUwNTg0MjAxMDIyMzgwODU2Mg.GUZQN8.e_tVXCkZFuQ7E6AOAz6ko8_TwRsQM7B1aKbdNA"

# YAHA APNE BOTS KE DISPLAY NAMES (Nicknames) DAALEIN
Ayesha = "Bot One"
Fahad = "Bot Two"

intents = discord.Intents.default()
intents.message_content = True

bot1 = commands.Bot(command_prefix="1!", intents=intents)
bot2 = commands.Bot(command_prefix="2!", intents=intents)

# Global variable taaki dono bots ko pata ho kis channel mein baat karni hai
active_channel_id = None

# Kisi bhi available text channel ko dhoondne ka function
def find_a_channel(bot):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel
    return None

@bot1.event
async def on_ready():
    global active_channel_id
    print(f'{bot1.user.name} (Bot 1) is Online!')
    
    await asyncio.sleep(5) # Bots ko stable hone dein
    channel = find_a_channel(bot1)
    
    if channel and active_channel_id is None:
        active_channel_id = channel.id
        print(f"Chatting started in channel: {channel.name}")
        await channel.send("Hello! Kaise ho?")

@bot2.event
async def on_ready():
    print(f'{bot2.user.name} (Bot 2) is Online!')

@bot1.event
async def on_message(message):
    global active_channel_id
    
    # Agar abhi tak koi channel set nahi hua, toh jo bhi pehla message aaye use hi channel maan lo
    if active_channel_id is None and not message.author.bot:
        active_channel_id = message.channel.id

    if message.channel.id != active_channel_id or message.author == bot1.user:
        return

    # Agar Bot 2 ne message bheja
    if message.author == bot2.user or message.author.display_name == BOT_2_DISPLAY_NAME:
        await asyncio.sleep(3)
        msg = message.content.lower()
        
        if "kaise ho" in msg:
            await message.channel.send("Main badhiya hoon! Tum batao?")
        elif "tum batao" in msg:
            await message.channel.send("Main bhi ekdum mast. Aur kya chal raha hai?")
        elif "chal raha hai" in msg:
            await message.channel.send("Bas server par bakchodi chal rahi hai 😂")
        else:
            await message.channel.send("Sahi hai bhai, aur sunao!")

@bot2.event
async def on_message(message):
    global active_channel_id

    if message.channel.id != active_channel_id or message.author == bot2.user:
        return

    # Agar Bot 1 ne message bheja
    if message.author == bot1.user or message.author.display_name == BOT_1_DISPLAY_NAME:
        await asyncio.sleep(3)
        msg = message.content.lower()
        
        if "hello" in msg:
            await message.channel.send("Hi! Kaise ho?")
        elif "badhiya hoon" in msg:
            await message.channel.send("Great! Aur batao?")
        elif "mast" in msg:
            await message.channel.send("Aur kya chal raha hai?")
        elif "bakchodi" in msg:
            await message.channel.send("Haha, sahi hai! Lage raho.")
        else:
            await message.channel.send("Aur sab badhiya?")

# Dono bots ko ek sath run karne ka function
async def main():
    Thread(target=run_web_server).start()
    await asyncio.gather(
        bot1.start(BOT_TOKEN_1),
        bot2.start(BOT_TOKEN_2)
    )

if __name__ == "__main__":
    asyncio.run(main())
