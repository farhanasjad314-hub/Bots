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
    return "Bots are running safely without IDs!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

server_thread = threading.Thread(target=run_web_server, daemon=True)
server_thread.start()

# ================= ⚙️ BOTS CONFIGURATION =================
BOT_1_TOKEN = os.environ.get("BOT_TOKEN_1")
BOT_2_TOKEN = os.environ.get("BOT_TOKEN_2")

bot1_name = "Fahad"
bot2_name = "Ayesha"

intents = discord.Intents.default()
intents.message_content = True

bot1 = commands.Bot(command_prefix="11", intents=intents)
bot2 = commands.Bot(command_prefix="21", intents=intents)

# ================= 🔍 AUTOMATIC CHANNEL FINDER =================
def find_any_text_channel(bot):
    # Bot jis bhi server mein hai, wahan ka pehla text channel dhoondega
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                return channel
    return None

# ================= 💬 SMART CHAT LOOP =================
async def start_infinite_chat(channel):
    await asyncio.sleep(5)
    print(f"🚀 CHAT LOOP STARTED IN CHANNEL: #{channel.name}")
    
    await channel.send(f"**{bot1_name}**: Hello Ayesha, kaisi ho? Kaafi dino baad baat ho rahi hai.")
    current_speaker = bot2_name
    
    while True:
        try:
            wait_time = random.randint(5, 12)
            await asyncio.sleep(wait_time)
            
            if current_speaker == bot1_name:
                replies = [
                    "Haha sahi baat hai, wese chal kya raha hai aaj kal?",
                    "Are nahi yaar, main toh bas thoda busy tha.",
                    "Kuch naya batao, koi achhi movie dekhi?",
                    "Haan wo toh hai, waise tumne khana khaya?",
                    "Achaaa, mujhe laga tum bhool gayi mujhe 😜",
                    "Chalo sahi hai, aur batao?"
                ]
                await channel.send(f"**{bot1_name}**: {random.choice(replies)}")
                current_speaker = bot2_name
                
            else:
                replies = [
                    "Main thik hoon! Tum batao, kahan gayab rehte ho?",
                    "Bas chal raha hai routine, tum sunao apni.",
                    "Nahi yaar, aaj kal bas padhai/kaam chal raha hai.",
                    "Haan abhi thodi der pehle hi khaya, tumne?",
                    "Suno na, ek mast cheez batati hoon ruko...",
                    "Hehe nahi bhooli yaar, tum batao."
                ]
                await channel.send(f"**{bot2_name}**: {random.choice(replies)}")
                current_speaker = bot1_name
                
        except Exception as e:
            print(f"Chat Loop Error: {e}")
            await asyncio.sleep(10)

@bot1.event
async def on_ready():
    print(f"✅ Bot 1 ({bot1_name}) Online!")
    await asyncio.sleep(3) # Server list load hone ka wait karein
    channel = find_any_text_channel(bot1)
    if channel:
        bot1.loop.create_task(start_infinite_chat(channel))
    else:
        print("❌ Error: Bots ko kisi channel mein bolne ki permission nahi hai!")

@bot2.event
async def on_ready():
    print(f"✅ Bot 2 ({bot2_name}) Online!")

# ================= 🚀 MAIN RUNNER =================
async def main():
    if not BOT_1_TOKEN or not BOT_2_TOKEN:
        print("❌ Error: Render variables missing!")
        return
    await asyncio.gather(
        bot1.start(BOT_1_TOKEN),
        bot2.start(BOT_2_TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main())
