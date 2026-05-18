
import discord
from discord.ext import commands
import asyncio
from flask import Flask
from threading import Thread

# Render ke liye background server
app = Flask('')

@app.route('/')
def home():
    return "Bots are running 24/7!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

# ----------------- BOTS SETUP -----------------

# YAHA APNE DONO BOTS KE TOKENS DAALEIN
BOT_TOKEN_1 = "YOUR_FIRST_BOT_TOKEN_HERE"
BOT_TOKEN_2 = "YOUR_SECOND_BOT_TOKEN_HERE"

# YAHA US CHANNEL KI ID DAALEIN JAHAN CHAT KARWANI HAI
CHANNEL_ID = 123456789012345678  # Apne channel ki ID se badlein

# YAHA APNE BOTS KE DISPLAY NAMES (Nicknames) DAALEIN
BOT_1_DISPLAY_NAME = "Bot One"
BOT_2_DISPLAY_NAME = "Bot Two"

intents = discord.Intents.default()
intents.message_content = True

bot1 = commands.Bot(command_prefix="1!", intents=intents)
bot2 = commands.Bot(command_prefix="2!", intents=intents)

# Dono bots ke beech chat chalu karne ka function
async def start_conversation(channel):
    await asyncio.sleep(5) # Thoda ruk kar shuru karein
    await channel.send("Hello! Kaise ho?")

@bot1.event
async def on_ready():
    print(f'{bot1.user.name} (Bot 1) is Online!')
    channel = bot1.get_channel(CHANNEL_ID)
    if channel:
        asyncio.create_task(start_conversation(channel))

@bot2.event
async def on_ready():
    print(f'{bot2.user.name} (Bot 2) is Online!')

@bot1.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author == bot1.user:
        return

    # Agar Bot 2 ne message bheja (Display Name ya User Name se check)
    if message.author == bot2.user or message.author.display_name == BOT_2_DISPLAY_NAME:
        await asyncio.sleep(3) # 3 second ka gap
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
    if message.channel.id != CHANNEL_ID or message.author == bot2.user:
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
    # Web server ko alag thread mein chalayein
    Thread(target=run_web_server).start()
    
    # Dono bots ko ek sath start karein
    await asyncio.gather(
        bot1.start(BOT_TOKEN_1),
        bot2.start(BOT_TOKEN_2)
    )

if __name__ == "__main__":
    asyncio.run(main())
