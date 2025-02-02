import os
import requests
from dotenv import load_dotenv
import random
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Load environment variables from .env file
load_dotenv()

# Constants
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
WEB_APP_URL = "http://13.51.204.40/web_app.html"  # Replace with your actual EC2 public IP/domain
IP_API_URL = "http://ip-api.com/json/{ip_address}"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

# Bible verses for encouragement
BIBLE_VERSES = [
    "🌟 Isaiah 41:10 - Do not fear, for I am with you; do not be dismayed, for I am your God.",
    "🌿 Psalm 23:4 - Even though I walk through the darkest valley, I will fear no evil, for you are with me.",
    "💪 Philippians 4:13 - I can do all things through Christ who strengthens me.",
]

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Function to fetch geolocation and ISP details
def get_geolocation_and_isp(ip_address):
    """
    Fetches geolocation and ISP details using the ip-api.com service.
    Returns a dictionary with location details or an error message.
    """
    try:
        response = requests.get(IP_API_URL.format(ip_address=ip_address), timeout=5)
        data = response.json()
        if data.get("status") == "fail":
            return {"error": data.get("message", "Unknown error")}
        return {
            "latitude": data.get("lat"),
            "longitude": data.get("lon"),
            "city": data.get("city"),
            "country": data.get("country"),
            "isp": data.get("isp"),
        }
    except Exception as e:
        logger.error(f"Error fetching geolocation: {e}")
        return {"error": f"Error fetching geolocation and ISP: {str(e)}"}

# Function to fetch weather information
def get_weather(lat, lon):
    """
    Fetches current weather data using OpenWeatherMap API.
    Returns a dictionary with weather details or an error message.
    """
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": OPENWEATHERMAP_API_KEY,
            "units": "metric",
        }
        response = requests.get(WEATHER_API_URL, params=params, timeout=5)
        data = response.json()
        if data.get("cod") != 200:  # Check for API errors
            return {"error": data.get("message", "Unknown error")}
        return {
            "weather": data["weather"][0]["description"].capitalize(),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "city": data["name"],
        }
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        return {"error": f"Error fetching weather data: {str(e)}"}

# Handler for /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Sends a welcome message with a button to fetch the user's IP address.
    """
    keyboard = [[InlineKeyboardButton("Get My IP", web_app=WebAppInfo(url=WEB_APP_URL))]]
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
    """
    Handles data received from the web app (e.g., user's IP address).
    """
    if update.message.web_app_data:
        ip_address = update.message.web_app_data.data
        context.user_data["ip_address"] = ip_address
        await update.message.reply_text(f"✅ Your public IP address has been set to `{ip_address}`.", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ Failed to retrieve your IP address. Please try again.")

# General function to display user info
async def display_info(update: Update, context: ContextTypes.DEFAULT_TYPE, show_weather=False):
    """
    Displays geolocation, ISP, and optionally weather information.
    """
    ip_address = context.user_data.get("ip_address")
    if not ip_address:
        await update.message.reply_text("❌ Please get your IP address first by clicking 'Get My IP' in the /start menu.")
        return

    geo_data = get_geolocation_and_isp(ip_address)
    if "error" in geo_data:
        await update.message.reply_text(f"❌ Error: {geo_data['error']}")
        return

    message = (
        f"🌐 Public IP Address: {ip_address}\n"
        f"📍 Latitude: {geo_data['latitude']}\n"
        f"📍 Longitude: {geo_data['longitude']}\n"
        f"🏙️ City: {geo_data['city']}\n"
        f"🌍 Country: {geo_data['country']}\n"
        f"🌐 ISP: {geo_data['isp']}"
    )

    if show_weather:
        weather_data = get_weather(geo_data['latitude'], geo_data['longitude'])
        if "error" not in weather_data:
            message += (
                f"\n🌤️ Weather in {weather_data['city']}: {weather_data['weather']}\n"
                f"Temperature: {weather_data['temperature']}°C, Humidity: {weather_data['humidity']}%"
            )
        else:
            message += f"\n❌ Weather Error: {weather_data['error']}"

    await update.message.reply_text(message)

# Command handlers
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays geolocation and ISP details."""
    await display_info(update, context, show_weather=False)

async def internet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays internet-related information."""
    await display_info(update, context, show_weather=False)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays weather information."""
    await display_info(update, context, show_weather=True)

async def display_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Displays all available information."""
    await display_info(update, context, show_weather=True)
    await update.message.reply_text(f"📖 Today's Encouraging Verse: {random.choice(BIBLE_VERSES)}")

# Main function to run the bot
def main():
    """
    Initializes and starts the Telegram bot.
    """
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    application.add_handler(CommandHandler("location", location))
    application.add_handler(CommandHandler("internet", internet))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("display_all", display_all))

    # Start the bot
    logger.info("🤖 Bot started...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()