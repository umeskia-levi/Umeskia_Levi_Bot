import os
import re
import requests
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Replace with your own Telegram Bot API token
TELEGRAM_BOT_TOKEN = "7571392688:AAEZkbvisM3FXhadpXwupnekdqZT3Cl6pno"
BOT_NAME = "@UMESKIA_LEVI_BOT"

# OpenWeatherMap API key (optional for weather-related features)
OPENWEATHERMAP_API_KEY = "86c509275b31c2e56706ab36b87ea0b7"

# List of Bible verses for encouragement
BIBLE_VERSES = [
    "🌟 Isaiah 41:10 - Do not fear, for I am with you; do not be dismayed, for I am your God.",
    "🌿 Psalm 23:4 - Even though I walk through the darkest valley, I will fear no evil, for you are with me.",
    "💪 Philippians 4:13 - I can do all things through Christ who strengthens me.",
    # Add more verses here...
]

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

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
    [InlineKeyboardButton("Get My IP", web_app=WebAppInfo(url="https://13.51.204.40/web_app.html"))]
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Hello! Use the following commands:\n"
        "/daily_devotion - Get a random Bible verse\n"
        "/location - Display your geolocation details\n"
        "/internet - Display internet-related information\n"
        "/display_all - Show everything on one page\n\n"
        "Click the butimport os
import re
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

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
    # Add more verses here...
]

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

# Function to get weather information using latitude and longitude
def get_weather(lat, lon):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            weather = data["weather"][0]["description"].capitalize()
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            city = data["name"]
            return {
                "weather": weather,
                "temperature": temperature,
                "humidity": humidity,
                "city": city,
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    return {"error": "Could not retrieve weather data"}

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Get My IP", web_app=WebAppInfo(url="http://13.51.204.40/web_app.html"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Hello! Use the following commands:\n"
        "/daily_devotion - Get a random Bible verse\n"
        "/location - Display your geolocation details\n"
        "/internet - Display internet-related information\n"
        "/weather - Get the current weather for your location\n"
        "/display_all - Show everything on one page\n\n"
        "Click the button below to allow me to fetch your IP address:",
        reply_markup=reply_markup,
    )

# Handler for receiving data from the web app
async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.web_app_data:
        ip_address = update.message.web_app_data.data
        context.user_data["ip_address"] = ip_address
        await update.message.reply_text(f"✅ Your public IP address has been set to `{ip_address}`.", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Failed to retrieve your IP address. Please try again.")

# Handler for the /location command
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
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
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
    isp = geolocation_and_isp.get("isp", "Unknown ISP") if "error" not in geolocation_and_isp else "Error retrieving ISP"
    message = (
        f"🌐 Public IP Address: {ip_address}\n"
        f"🌐 ISP: {isp}"
    )
    await update.message.reply_text(message)

# Handler for the /weather command
async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
    if "error" in geolocation_and_isp:
        await update.message.reply_text(f"❌ Geolocation Error: {geolocation_and_isp['error']}")
        return
    latitude = geolocation_and_isp.get("latitude")
    longitude = geolocation_and_isp.get("longitude")
    weather_data = get_weather(latitude, longitude)
    if "error" in weather_data:
        await update.message.reply_text(f"❌ Weather Error: {weather_data['error']}")
        return
    city = weather_data.get("city")
    weather_desc = weather_data.get("weather")
    temperature = weather_data.get("temperature")
    humidity = weather_data.get("humidity")
    message = (
        f"🌤️ Current Weather in {city}:\n"
        f"Description: {weather_desc}\n"
        f"Temperature: {temperature}°C\n"
        f"Humidity: {humidity}%"
    )
    await update.message.reply_text(message)

# Handler for the /display_all command
async def display_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
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
    weather_data = get_weather(latitude, longitude) if "error" not in geolocation_and_isp else None
    weather_message = ""
    if weather_data and "error" not in weather_data:
        weather_message = (
            f"\n🌤️ Current Weather in {weather_data.get('city')}:\n"
            f"Description: {weather_data.get('weather')}\n"
            f"Temperature: {weather_data.get('temperature')}°C\n"
            f"Humidity: {weather_data.get('humidity')}%"
        )
    elif weather_data and "error" in weather_data:
        weather_message = f"\n❌ Weather Error: {weather_data['error']}"

    bible_verse = random.choice(BIBLE_VERSES)
    message = (
        f"📊 Here is your device information:\n\n"
        f"🌐 Public IP Address: {ip_address}\n\n"
        f"📍 Geolocation and ISP:\n{geo_message}{weather_message}\n\n"
        f"📖 Encouragement for Today:\n{bible_verse}\n\n"
        f"🙏 Thank you for using {BOT_NAME}! ❤️"
    )
    await update.message.reply_text(message)

# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    application.add_handler(CommandHandler("location", location))
    application.add_handler(CommandHandler("internet", internet))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("display_all", display_all))

    # Start the bot
    print("🤖 Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()ton below to allow me to fetch your IP address:",
        reply_markup=reply_markup,
    )

# Handler for receiving data from the web app
async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.web_app_data:
        ip_address = update.message.web_app_data.data
        context.user_data["ip_address"] = ip_address
        await update.message.reply_text(f"✅ Your public IP address has been set to `{ip_address}`.", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Failed to retrieve your IP address. Please try again.")

# Handler for the /location command
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
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
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
    isp = geolocation_and_isp.get("isp", "Unknown ISP") if "error" not in geolocation_and_isp else "Error retrieving ISP"
    message = (
        f"🌐 Public IP Address: {ip_address}\n"
        f"🌐 ISP: {isp}"
    )
    await update.message.reply_text(message)

# Handler for the /display_all command
async def display_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ You haven't set your public IP address yet. Click 'Get My IP' in the /start menu.", parse_mode="Markdown")
        return
    geolocation_and_isp = get_geolocation_and_isp(ip_address)
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
    bible_verse = random.choice(BIBLE_VERSES)
    message = (
        f"📊 Here is your device information:\n\n"
        f"🌐 Public IP Address: {ip_address}\n\n"
        f"📍 Geolocation and ISP:\n{geo_message}\n\n"
        f"📖 Encouragement for Today:\n{bible_verse}\n\n"
        f"🙏 Thank you for using {BOT_NAME}! ❤️"
    )
    await update.message.reply_text(message)

# Main function to run the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    application.add_handler(CommandHandler("location", location))
    application.add_handler(CommandHandler("internet", internet))
    application.add_handler(CommandHandler("display_all", display_all))
    # Start the bot
    print("🤖 Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()