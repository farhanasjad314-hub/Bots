import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
import threading

# ================= 🌐 WEB SERVER SETUP FOR RENDER =================
app = Flask('')

@app.route('/')
def home():
    return "Bots are running 24/7 perfectly!"

def run_web_server():
    # Render jo port bhejega (jaise 8080 ya 10000), ye use automatic pakad lega
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Web server ko background thread mein start karna taaki port active rahe
server_thread = threading.Thread(target=run_web_server, daemon=True)
server_thread.start()

# ================= ⚙️ BOTS CONFIGURATION =================
# Ab tokens direct Render ke Environment Variables se load honge
BOT_1_TOKEN = os.environ.get("MTUwNTg0MjU5NDM3MzA0NjMxMw.G7k_LC.pDiIYFaJYq5_xU11kYEZx1OFRaNGGzdh4wwSjc")
BOT_2_TOKEN = os.environ.get("MTUwNTg0MjAxMDIyMzgwODU2Mg.GtKhJj.TGikwiLuaCX7b0UheUzb-WdMa9CK3Oxbyys8x8")

# Yahan apne channel ki ID daal dena jahan chat karwani hai
CHANNEL_ID = 123456789012345678  # 👈 Apni sahi ID se replace karein

# Bots ke display names (Nicknames)
Ayesha = "Bot One"
Fahad = "Bot Two"

intents = discord.Intents.default()
intents.message_content = True

bot1 = commands.Bot(command_prefix="11", intents=intents)
bot2 = commands.Bot(command_prefix="21", intents=intents)

# Global variable dono bots ke chat sync ke liye
active_channel_id = None

# ================= 💬 AUTOMATIC CHAT FUNCTION =================
async def start_conversation(channel):
    await asyncio.sleep(5)  # Thoda ruk kar shuru karein
    await channel.send("Hello! Kaise ho?")

@bot1.event
async def on_ready():
    print(f"✅ Bot 1 Online as {bot1.user}")
    channel = bot1.get_channel(CHANNEL_ID)
    if channel:
        bot1.loop.create_task(start_conversation(channel))
    else:
        print("❌ Bot 1 ko channel nahi mila. Channel ID check karein.")

@bot2.event
async def on_ready():
    print(f"✅ Bot 2 Online as {bot2.user}")

# ================= 🚀 MAIN RUNNER =================
async def main():
    if not BOT_1_TOKEN or not BOT_2_TOKEN:
        print("❌ Error: BOT_TOKEN_1 ya BOT_TOKEN_2 Render ki settings mein nahi mila!")
        return
        
    await asyncio.gather(
        bot1.start(BOT_1_TOKEN),
        bot2.start(BOT_2_TOKEN)
    )

if __name__ == "__main__":
    asyncio.run(main())
