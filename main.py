
import discord
from discord.ext import commands
import asyncio
import os
import random
from flask import Flask
import threading

# ================= 🌐 WEB SERVER FOR RENDER =================
app = Flask('')

@app.route('/')
def home():
    return "Bots are running perfectly!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

server_thread = threading.Thread(target=run_web_server, daemon=True)
server_thread.start()

# ================= ⚙️ BOTS CONFIGURATION =================
BOT_1_TOKEN = os.environ.get("BOT_TOKEN_1")
BOT_2_TOKEN = os.environ.get("BOT_TOKEN_2")
TARGET_CHANNEL_NAME = "chat"  # 👈 Yahan apne us channel ka naam likho jahan bots ko bolna hai

bot1_name = "Fahad"
bot2_name = "Ayesha"

intents = discord.Intents.default()
intents.message_content = True

bot1 = commands.Bot(command_prefix="11", intents=intents)
bot2 = commands.Bot(command_prefix="21", intents=intents)

# ================= 🔍 CHANNEL FINDER =================
def find_target_channel(bot):
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.name.lower() == TARGET_CHANNEL_NAME.lower():
                if channel.permissions_for(guild.me).send_messages:
                    return channel
    return None

# ================= 💬 SMART CHAT LOOP =================
async def start_infinite_chat(channel):
    await asyncio.sleep(8)
    print(f"🚀 Chatting started in: #{channel.name}")
    
    await channel.send(f"**{bot1_name}**: Hello Ayesha, kaisi ho?")
    current_speaker = bot2_name
    
    while True:
        try:
            await asyncio.sleep(random.randint(6, 15))
            if current_speaker == bot1_name:
                replies = ["Haha sahi baat hai, wese chal kya raha hai aaj kal?", "Are nahi yaar, main toh bas thoda busy tha.", "Kuch naya batao, koi achhi movie dekhi?", "Haan wo toh hai, waise tumne khana khaya?", "Achaaa, mujhe laga tum bhool gayi mujhe 😜"]
                await channel.send(f"**{bot1_name}**: {random.choice(replies)}")
                current_speaker = bot2_name
            else:
                replies = ["Main thik hoon! Tum batao, kahan gayab rehte ho?", "Bas chal raha hai routine, tum sunao apni.", "Nahi yaar, aaj kal bas padhai/kaam chal raha hai.", "Haan abhi thodi der pehle hi khaya, tumne?", "Hehe nahi bhooli yaar, tum batao."]
                await channel.send(f"**{bot2_name}**: {random.choice(replies)}")
                current_speaker = bot1_name
        except Exception as e:
            print(f"Loop Error: {e}")
            await asyncio.sleep(10)

# ================= 🤖 BOT EVENTS =================
@bot1.event
async def on_ready():
    print(f"✅ {bot1_name} is online!")
    await asyncio.sleep(5)
    channel = find_target_channel(bot1)
    if channel:
        bot1.loop.create_task(start_infinite_chat(channel))

@bot2.event
async def on_ready():
    print(f"✅ {bot2_name} is online!")

@bot1.event
async def on_guild_join(guild):
    print(f"Joined new server: {guild.name}")

# ================= 🚀 MAIN RUNNER =================
async def main():
    if not BOT_1_TOKEN or not BOT_2_TOKEN:
        print("❌ Error: Tokens missing in Render!")
        return
    await asyncio.gather(bot1.start(BOT_1_TOKEN), bot2.start(BOT_2_TOKEN))

if __name__ == "__main__":
    asyncio.run(main())
