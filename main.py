import discord
from discord.ext import commands
import asyncio
import os
import random

# CONFIGURATION
TOKEN = os.environ.get("BOT_TOKEN_1")
TARGET_ID = int(os.environ.get("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Images ke Direct Links (Google ya Imgur se copy kiye huye)
FAHAD_PFP = "https://i.imgur.com/8QzN9mK.png" # Yahan apni link daal do
AYESHA_PFP = "https://i.imgur.com/k9v8N7m.png" # Yahan apni link daal do

chat_task = None

async def get_webhook(channel):
    webhooks = await channel.webhooks()
    for webhook in webhooks:
        if webhook.user.id == bot.user.id:
            return webhook
    return await channel.create_webhook(name="ChatBot")

async def chat_loop(channel):
    webhook = await get_webhook(channel)
    while True:
        # Fahad Ka Message
        await webhook.send("Hello Ayesha, kaisi ho?", username="Fahad", avatar_url=FAHAD_PFP)
        await asyncio.sleep(random.randint(6, 10))
        # Ayesha Ka Message
        await webhook.send("Main thik hoon! Tum sunao, kya chal raha hai?", username="Ayesha", avatar_url=AYESHA_PFP)
        await asyncio.sleep(random.randint(6, 10))

@bot.command()
async def startchat(ctx):
    global chat_task
    if ctx.channel.id == TARGET_ID:
        if chat_task is None:
            chat_task = bot.loop.create_task(chat_loop(ctx.channel))
            await ctx.send("✅ Chat shuru!")
        else:
            await ctx.send("⚠️ Chat pehle se chal rahi hai!")
    else:
        await ctx.send("❌ Galat channel!")

@bot.command()
async def stopchat(ctx):
    global chat_task
    if chat_task:
        chat_task.cancel()
        chat_task = None
        await ctx.send("🛑 Chat ruk gayi.")

bot.run(TOKEN)
