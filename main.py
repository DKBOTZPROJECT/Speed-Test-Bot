from pyrogram import Client, filters
from pyrogram.types import Message
import speedtest
import psutil
import platform
import shutil

API_ID = 10956858
API_HASH = "cceefd3382b44d4d85be2d83201102b7"
BOT_TOKEN = "7347629693:AAFG5Sl5_eV-aj_e6JNGnuOA08yhpmvU2PI"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text("👋 Hello! I'm your bot.\n\nUse /help to see what I can do!")

# Help Command
@app.on_message(filters.command("help") & filters.private)
async def help_command(client, message: Message):
    await message.reply_text("""
🛠 **Help Menu**:
/start - Welcome message
/help - Show this help
/about - About the bot
/speedtest - Run speed + system test
""")

# About Command
@app.on_message(filters.command("about") & filters.private)
async def about_command(client, message: Message):
    await message.reply_text("🤖 This is a demo Telegram bot built using Pyrogram!")


# Speedtest Command
@app.on_message(filters.command("speedtest") & filters.private)
async def speed_test(client, message: Message):
    msg = await message.reply_text("⚡ Running speed test, please wait...")

    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download()
        upload = st.upload()
        server = st.get_best_server()

        # Convert speed to Mbps
        download_mbps = round(download / 10**6, 2)
        upload_mbps = round(upload / 10**6, 2)

        # Disk info
        total, used, free = shutil.disk_usage("/")
        total_gb = round(total / (1024 ** 3), 2)
        used_gb = round(used / (1024 ** 3), 2)
        free_gb = round(free / (1024 ** 3), 2)

        text = f"""
📡 **Speed Test Result**:

**Server**: {server['host']}
**Sponsor**: {server['sponsor']}
**Location**: {server['name']}, {server['country']}
**Ping**: {server['latency']} ms

⬇️ **Download**: {download_mbps} Mbps  
⬆️ **Upload**: {upload_mbps} Mbps

💾 **Storage**:
• Total: {total_gb} GB
• Used : {used_gb} GB
• Free : {free_gb} GB

🖥 **System**: {platform.system()} {platform.release()}
    """

        await msg.edit_text(text)
    except Exception as e:
        await msg.edit_text(f"❌ Error while running speedtest:\n`{e}`")

# Run the Bot
app.run()
