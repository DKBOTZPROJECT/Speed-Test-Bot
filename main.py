from pyrogram import Client, filters
from pyrogram.types import Message
import speedtest
import psutil
import platform
import shutil
import socket
import time
import os
from datetime import timedelta

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text("<b>👋 Welcome!</b>\n\n<i>I Am A Powerful Speed Test Bot 🚀</i>\n\n⚡ Test your <b>Internet Speed</b>\n💻 Check <b>System Performance</b>\n📊 Get Accurate <b>Upload / Download / Ping</b>\n\n<b>📌 Use</b> /help <b>To See All Commands</b>")


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
async def full_speed_test(client, message: Message):
    msg = await message.reply_text("⚡ Running full speed and system test, please wait...")

    try:
        # Speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download()
        upload = st.upload()
        server = st.get_best_server()
        download_mbps = round(download / 10**6, 2)
        upload_mbps = round(upload / 10**6, 2)

        # Disk Info
        total, used, free = shutil.disk_usage("/")
        total_gb = round(total / (1024**3), 2)
        used_gb = round(used / (1024**3), 2)
        free_gb = round(free / (1024**3), 2)

        # CPU Info
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_cores = psutil.cpu_count(logical=True)
        cpu_name = platform.processor()

        # RAM Info
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024**3), 2)
        ram_used = round(ram.used / (1024**3), 2)
        ram_free = round(ram.available / (1024**3), 2)
        ram_percent = ram.percent

        # Uptime
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_str = str(timedelta(seconds=int(uptime_seconds)))

        # Host Info
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        text = f"""
📡 **Speed Test Result**:

**🌐 Server**: {server['host']}
**🌍 Location**: {server['name']}, {server['country']}
**🏢 Sponsor**: {server['sponsor']}
**📶 Ping**: {server['latency']} ms

⬇️ **Download**: {download_mbps} Mbps  
⬆️ **Upload**: {upload_mbps} Mbps

🧠 **CPU Info**:
• Cores: {cpu_cores}
• Usage: {cpu_percent}%
• Name : {cpu_name}

💾 **Disk Info**:
• Total: {total_gb} GB
• Used : {used_gb} GB
• Free : {free_gb} GB

🧠 **RAM Info**:
• Total: {ram_total} GB
• Used : {ram_used} GB
• Free : {ram_free} GB
• Usage: {ram_percent}%

🖥 **System Info**:
• OS     : {system} {release}
• Machine: {machine}
• Host   : {hostname}
• IP     : {ip_address}

⏱ **Uptime**: {uptime_str}
        """

        await msg.edit_text(text)
    except Exception as e:
        await msg.edit_text(f"❌ Error during speedtest:\n`{e}`")
# Run the Bot
app.run()
