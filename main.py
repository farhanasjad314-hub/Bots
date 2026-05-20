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
def home(): return "Bots are waiting for command!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web_server, daemon=True).start()

# Configuration
BOT_1_TOKEN = os.environ.get("BOT_TOKEN_1")
BOT_2_TOKEN = os.environ.get("BOT_TOKEN_2")
TARGET_ID = int(os.environ.get("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot1 = commands.Bot(command_prefix="!", intents=intents)
bot2 = commands.Bot(command_prefix="!", intents=intents)

# Chat loop function
async def chat_loop(channel):
    await channel.send("🤖 **System**: Chatting start ho gayi hai!")
    while True:
        await channel.send("**Fahad**: Hello Ayesha, kaisi ho?")
        await asyncio.sleep(random.randint(8, 12))
        await channel.send("**Ayesha**: Main thik hoon! Tum sunao, kya chal raha hai?")
        await asyncio.sleep(random.randint(8, 12))

# Command trigger
@bot1.command(name="startchat")
async def startchat(ctx):
    if ctx.channel.id == TARGET_ID:
        bot1.loop.create_task(chat_loop(ctx.channel))
    else:
        await ctx.send("❌ Yeh command sirf mere assigned channel mein kaam karega!")

@bot1.event
async def on_ready():
    print(f"✅ Fahad Online! Type !startchat to begin.")

@bot2.event
async def on_ready():
    print(f"✅ Ayesha Online!")

async def main():
    await asyncio.gather(bot1.start(BOT_1_TOKEN), bot2.start(BOT_2_TOKEN))

if __name__ == "__main__":
    asyncio.run(main())
