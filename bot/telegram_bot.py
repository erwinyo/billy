# Built-in imports
from typing import Final

# Third-party imports
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
)


# Local imports


# Billy Telegram Bot
BOT_URL = "t.me/billyofficialbot"
BOT_USERNAME = "@billyofficialbot"
BOT_TOKEN = "7970533350:AAGMEB9AMtnDWM3_jlXECFeQsqw35uOAAbM"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! Welcome to the bot. Use /help to see available commands."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/echo <message> - Echo back the message you send"
    )
    await update.message.reply_text(help_text)


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This is a custom command response!")


# Responses
def handle_response(text: str) -> str:
    processed = text.strip().lower()
    return f"Received Processed: {processed}"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"User ({update.message.chat.id}) in {message_type}: {text}")
    if message_type == "group":
        if BOT_USERNAME in text:  # Check if the bot username is mentioned
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str
    else:
        response: str = handle_response(text)

    print(f"Bot Response: {response}")
    await update.message.reply_text(response)


# Logging error
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")


if __name__ == "__main__":
    # Create the application
    print("Initializing Telegram bot...")
    application: Application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("custom", custom_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    application.add_error_handler(error)

    # Run the bot
    print(f"Starting bot at {BOT_URL} with token {BOT_TOKEN}")
    print("Pooling...")
    application.run_polling(poll_interval=3)
