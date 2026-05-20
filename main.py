import discord
from discord.ext import commands
import asyncio
import os
import random
from flask import Flask
import threading

# ================= 🌐 WEB SERVER FOR RENDER (PORT FIX) =================
app = Flask('')

@app.route('/')
def home():
    return "Bots are running safely 24/7!"

def run_web_server():
    # Render jo bhi port dega, ye use automatic detect kar lega
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Web server ko background thread mein start karna taaki Render live rahe
server_thread = threading.Thread(target=run_web_server, daemon=True)
server_thread.start()

# ================= ⚙️ BOTS CONFIGURATION =================
# Tokens ab Render ke Environment Variables se automatic uthaye jayenge (100% SAFE)
BOT_1_TOKEN = os.environ.get("BOT_TOKEN_1")
BOT_2_TOKEN = os.environ.get("BOT_TOKEN_2")

# ⚠️ YAHAN APNE DISCORD CHANNEL KI ID DAALEIN JAHAN CHAT KARWANI HAI
CHANNEL_ID = 123456789012345678  # 👈 Is number ko mita kar apni sahi Channel ID likhein

# Bots ke nicknames
bot1_name = "Fahad"
bot2_name = "Ayesha"

intents = discord.Intents.default()
intents.message_content = True

bot1 = commands.Bot(command_prefix="11", intents=intents)
bot2 = commands.Bot(command_prefix="21", intents=intents)

# ================= 💬 SMART AUTOMATIC CHAT LOOP =================
async def start_infinite_chat(channel):
    await asyncio.sleep(10) # Bots ko properly connect hone ka time dein
    print("🚀 AUTOMATIC CHAT LOOP STARTED!")
    
    # Starting message
    await channel.send(f"**{bot1_name}**: Hello Ayesha, kaisi ho? Kaafi dino baad baat ho rahi hai.")
    current_speaker = bot2_name
    
    # Ye loop bina ruke chalta rahega
    while True:
        try:
            # Discord anti-spam se bachne ke liye har baar 5 se 12 second ka RANDOM delay
            wait_time = random.randint(5, 12)
            await asyncio.sleep(wait_time)
            
            if current_speaker == bot1_name:
                # Fahad ke random replies
                replies = [
                    "Haha sahi baat hai, wese chal kya raha hai aaj kal?",
                    "Are nahi yaar, main toh bas thoda busy tha.",
                    "Kuch naya batao, koi achhi movie dekhi?",
                    "Haan wo toh hai, waise tumne khana khaya?",
                    "Achaaa, mujhe laga tum bhool gayi mujhe 😜",
                    "Chalo sahi hai, aur batao?"
                ]
                msg = random.choice(replies)
                await channel.send(f"**{bot1_name}**: {msg}")
                current_speaker = bot2_name # Agli baari Ayesha ki
                
            else:
                # Ayesha ke random replies
                replies = [
                    "Main thik hoon! Tum batao, kahan gayab rehte ho?",
                    "Bas chal raha hai routine, tum sunao apni.",
                    "Nahi yaar, aaj kal bas padhai/kaam chal raha hai.",
                    "Haan abhi thodi der pehle hi khaya, tumne?",
                    "Suno na, ek mast cheez batati hoon ruko...",
                    "Hehe nahi bhooli yaar, tum batao."
                ]
                msg = random.choice(replies)
                await channel.send(f"**{bot2_name}**: {msg}")
                current_speaker = bot1_name # Agli baari Fahad ki
                
        except Exception as e:
            print(f"Chat Loop Error: {e}")
            await asyncio.sleep(10)

@bot1.event
async def on_ready():
    print(f"✅ Bot 1 ({bot1_name}) Online!")
    channel = bot1.get_channel(CHANNEL_ID)
    if channel:
        bot1.loop.create_task(start_infinite_chat(channel))
    else:
        print("❌ Error: Bot 1 ko channel nahi mila. Channel ID check karein.")

@bot2.event
async def on_ready():
    print(f"✅ Bot 2 ({bot2_name}) Online!")

# ================= 🚀 MAIN RUNNER =================
async def main():
    if not BOT_1_TOKEN or not BOT_2_TOKEN:
        print("❌ Error: Render ke Environment Variables mein BOT_TOKEN_1 ya BOT_TOKEN_2 nahi mila!")
        return
        
    await asyncio.gather(
        bot1.start(BOT_1_TOKEN),
        bot2.start(BOT_2_TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main())
