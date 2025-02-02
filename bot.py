import os
import re
import requests
import uuid
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import speedtest
import random

# Replace with your own Telegram Bot API token
TELEGRAM_BOT_TOKEN = "7571392688:AAEZkbvisM3FXhadpXwupnekdqZT3Cl6pno"
BOT_NAME = "@UMESKIA_LEVI_BOT"

# OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = "86c509275b31c2e56706ab36b87ea0b7"

# List of Bible verses for encouragement
BIBLE_VERSES = [
    "🌟 Isaiah 41:10 - Do not fear, for I am with you; do not be dismayed, for I am your God.",
    "🌿 Psalm 23:4 - Even though I walk through the darkest valley, I will fear no evil, for you are with me.",
    "💪 Philippians 4:13 - I can do all things through Christ who strengthens me.",
    "🌈 Jeremiah 29:11 - For I know the plans I have for you, plans to prosper you and not to harm you.",
    "☀️ Matthew 6:34 - Therefore do not worry about tomorrow, for tomorrow will worry about itself.",
    "🕊 Romans 8:28 - And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
    "🌻 2 Corinthians 12:9 - But he said to me, “My grace is sufficient for you, for my power is made perfect in weakness.” Therefore I will boast all the more gladly of my weaknesses, so that the power of Christ may rest upon me.",
    "🌺 Isaiah 40:31 - But those who hope in the Lord will renew their strength. They will soar on wings like eagles; they will run and not grow weary, they will walk and not be faint.",
    "🌱 1 Peter 5:7 - Cast all your anxiety on him because he cares for you.",
    "🌄 Romans 15:13 - May the God of hope fill you with all joy and peace as you trust in him, so that you may overflow with hope by the power of the Holy Spirit.",
    "🙏 Psalm 46:1 - God is our refuge and strength, an ever-present help in trouble.",
    "🌼 Deuteronomy 31:6 - Be strong and courageous. Do not be afraid or terrified because of them, for the Lord your God goes with you; he will never leave you nor forsake you."
]


# Function to get the device's public IP address
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            return response.json().get("ip")
    except Exception as e:
        print(f"Error fetching public IP: {e}")
    return "Could not retrieve IP"

# Function to get the MAC address of the device
def get_mac_address():
    mac_addr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return mac_addr

# Function to get geolocation and ISP details using IP address
def get_geolocation_and_isp(ip_address):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "fail":
                return {"error": data["message"]}
            return {
                "latitude": data.get("lat"),
                "longitude": data.get("lon"),
                "city": data.get("city"),
                "country": data.get("country"),
                "isp": data.get("isp"),
            }
    except Exception as e:
        print(f"Error fetching geolocation and ISP: {e}")
    return {"error": "Could not retrieve geolocation or ISP"}

# Function to measure internet speed
def measure_internet_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = round(st.download() / 1_000_000, 2)
        upload_speed = round(st.upload() / 1_000_000, 2)
        ping = st.results.ping
        return {
            "download": download_speed,
            "upload": upload_speed,
            "ping": ping,
        }
    except Exception as e:
        print(f"Error measuring internet speed: {e}")
    return {"error": "Could not measure internet speed"}

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 Hello, {user.first_name}! Use the following commands:\n"
        "/daily_devotion - Get a random Bible verse\n"
        "/location - Display geolocation details\n"
        "/internet - Display internet-related information\n"
        "/display_all - Show everything on one page"
    )

# Handler for the /daily_devotion command
async def daily_devotion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bible_verse = random.choice(BIBLE_VERSES)  # Get a random Bible verse
    message = (
        f"📖 Daily Devotion for {user.first_name}:\n\n"
        f"{bible_verse}\n\n"
        f"🌟 May this verse inspire and guide you today! 🙏"
    )
    await update.message.reply_text(message)

# Handler for the /location command
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip_address = get_public_ip()
    geolocation_and_isp = get_geolocation_and_isp(ip_address)

    if "error" in geolocation_and_isp:
        geo_message = f"❌ Geolocation Error: {geolocation_and_isp['error']}"
    else:
        latitude = geolocation_and_isp.get("latitude")
        longitude = geolocation_and_isp.get("longitude")
        city = geolocation_and_isp.get("city")
        country = geolocation_and_isp.get("country")

        geo_message = (
            f"📍 Latitude: {latitude}\n"
            f"📍 Longitude: {longitude}\n"
            f"🏙️ City: {city}\n"
            f"🌍 Country: {country}"
        )

    await update.message.reply_text(
        f"📍 Here is your geolocation information:\n\n{geo_message}"
    )

# Handler for the /internet command
async def internet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip_address = get_public_ip()
    mac_address = get_mac_address()
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
    speed_info = measure_internet_speed()

    isp = geolocation_and_isp.get("isp", "Unknown ISP") if "error" not in geolocation_and_isp else "Error retrieving ISP"

    if "error" in speed_info:
        speed_message = f"⚠️ Speed Test Error: {speed_info['error']}"
    else:
        speed_message = (
            f"⬇️ Download Speed: {speed_info.get('download')} Mbps\n"
            f"⬆️ Upload Speed: {speed_info.get('upload')} Mbps\n"
            f"🏓 Ping: {speed_info.get('ping')} ms"
        )

    message = (
        f"🌐 Public IP Address: {ip_address}\n"
        f"🖲️ MAC Address: {mac_address}\n"
        f"🌐 ISP: {isp}\n\n"
        f"🚀 Internet Speed:\n{speed_message}"
    )

    await update.message.reply_text(message)

# Handler for the /display_all command
async def display_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ip_address = get_public_ip()
    mac_address = get_mac_address()
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
    speed_info = measure_internet_speed()

    if "error" in geolocation_and_isp:
        geo_message = f"❌ Geolocation/ISP Error: {geolocation_and_isp['error']}"
    else:
        latitude = geolocation_and_isp.get("latitude")
        longitude = geolocation_and_isp.get("longitude")
        city = geolocation_and_isp.get("city")
        country = geolocation_and_isp.get("country")
        isp = geolocation_and_isp.get("isp")

        geo_message = (
            f"📍 Latitude: {latitude}\n"
            f"📍 Longitude: {longitude}\n"
            f"🏙️ City: {city}\n"
            f"🌍 Country: {country}\n"
            f"🌐 ISP: {isp}"
        )

    if "error" in speed_info:
        speed_message = f"⚠️ Speed Test Error: {speed_info['error']}"
    else:
        speed_message = (
            f"⬇️ Download Speed: {speed_info.get('download')} Mbps\n"
            f"⬆️ Upload Speed: {speed_info.get('upload')} Mbps\n"
            f"🏓 Ping: {speed_info.get('ping')} ms"
        )

    bible_verse = random.choice(BIBLE_VERSES)

    message = (
        f"📊 Here is your device information:\n\n"
        f"🌐 Public IP Address: {ip_address}\n"
        f"🖲️ MAC Address: {mac_address}\n\n"
        f"📍 Geolocation and ISP:\n{geo_message}\n\n"
        f"🚀 Internet Speed:\n{speed_message}\n\n"
        f"📖 Encouragement for Today:\n{bible_verse}\n\n"
        f"🙏 Thank you for using {BOT_NAME}! ❤️"
    )

    await update.message.reply_text(message)

# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("daily_devotion", daily_devotion))
    application.add_handler(CommandHandler("location", location))
    application.add_handler(CommandHandler("internet", internet))
    application.add_handler(CommandHandler("display_all", display_all))

    # Start the bot
    print("🤖 Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()