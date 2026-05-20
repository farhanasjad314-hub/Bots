import discord
from discord.ext import commands
import asyncio
import os
import random
from flask import Flask
import threading

app = Flask('')
@app.route('/')
def home(): return "Bots are waiting!"
threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080))), daemon=True).start()

BOT_1_TOKEN = os.environ.get("BOT_TOKEN_1")
TARGET_ID = int(os.environ.get("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix="!", intents=intents)

# Chat control
chat_task = None

async def chat_loop(channel):
    while True:
        await channel.send("**Fahad**: Hello Ayesha, kaisi ho?")
        await asyncio.sleep(random.randint(6, 10))
        await channel.send("**Ayesha**: Main thik hoon! Tum sunao, kya chal raha hai?")
        await asyncio.sleep(random.randint(6, 10))

@bot.command()
async def startchat(ctx):
    global chat_task
    if ctx.channel.id == TARGET_ID:
        # Agar pehle se chat chal rahi hai, toh use cancel karo
        if chat_task:
            chat_task.cancel()
        
        await ctx.send("🤖 **System**: Chatting shuru ho gayi!")
        chat_task = bot.loop.create_task(chat_loop(ctx.channel))
    else:
        await ctx.send("❌ Galat channel!")

@bot.command()
async def stopchat(ctx):
    global chat_task
    if chat_task:
        chat_task.cancel()
        chat_task = None
        await ctx.send("🛑 **System**: Chat ruk gayi.")

@bot.event
async def on_ready():
    print(f"✅ Bot is Online!")

bot.run(BOT_1_TOKEN)
