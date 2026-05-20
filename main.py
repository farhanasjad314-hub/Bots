import discord
from discord.ext import commands
import asyncio
import os
import random
from flask import Flask
import threading

# Web server
app = Flask('')
@app.route('/')
def home(): return "Bots are online!"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))), daemon=True).start()

# Configuration
BOT_1_TOKEN = os.environ.get("BOT_TOKEN_1")
BOT_2_TOKEN = os.environ.get("BOT_TOKEN_2")
TARGET_ID = int(os.environ.get("CHANNEL_ID"))

# Intents setup (IMPORTANT: Message content zaruri hai)
intents = discord.Intents.default()
intents.message_content = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Chatting Control
is_chatting = False

@bot.command()
async def startchat(ctx):
    global is_chatting
    if ctx.channel.id == TARGET_ID:
        is_chatting = True
        await ctx.send("🤖 **System**: Chatting shuru ho gayi!")
        
        while is_chatting:
            await ctx.send("**Fahad**: Hello Ayesha, kaisi ho?")
            await asyncio.sleep(random.randint(6, 10))
            await ctx.send("**Ayesha**: Main thik hoon! Tum sunao, kya chal raha hai?")
            await asyncio.sleep(random.randint(6, 10))
    else:
        await ctx.send("❌ Yeh command sirf assigned channel mein kaam karega!")

@bot.command()
async def stopchat(ctx):
    global is_chatting
    is_chatting = False
    await ctx.send("🛑 **System**: Chat ruk gayi.")

@bot.event
async def on_ready():
    print(f"✅ Both bots managed by main bot are online!")

# Token management (Donon bots ka token)
async def main():
    # Yahan hum 2 bots ko run kar rahe hain
    await bot.start(BOT_1_TOKEN) 
    # Note: Agar 2 alag bot objects chahiye, toh code thoda aur complex hoga, 
    # filhaal test ke liye check karein ki ye command leta hai ya nahi.

if __name__ == "__main__":
    asyncio.run(main())
