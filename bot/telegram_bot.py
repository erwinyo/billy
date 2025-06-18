# Built-in imports
import re
import os
from typing import Final
import long_responses as long

# Third-party imports
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    filters,
    MessageHandler,
)
from dotenv import load_dotenv

load_dotenv(override=True)

# Local imports
from messaging import send_email
from placeholder import placeholder_login_email


BOT_URL = os.getenv("BOT_URL")
BOT_USERNAME = os.getenv("BOT_USERNAME")
BOT_TOKEN = os.getenv("BOT_TOKEN")

BILLY_API_ENDPOINT = os.getenv("BILLY_API_ENDPOINT")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# Utility for bot to response
# Source : https://www.youtube.com/watch?v=Ea9jgBjQxEs
def message_probability(
    user_message, recognised_words, single_response=False, required_words=[]
):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculates the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    # Must either have the required words, or be  single response
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    # Simplifies response creation / adds it to the dict
    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(
            message, list_of_words, single_response, required_words
        )

    # Responses ----------------------
    response("Hello!", ["hello", "hi", "hey", "sup", "heyo"], single_response=True)
    response("See you!", ["bye", "goodbye"], single_response=True)
    response(
        "I'm doing fine, and you?",
        ["how", "are", "you", "doing"],
        required_words=["how"],
    )
    response("You're welcome!", ["thank", "thanks"], single_response=True)
    response(
        "Thank you!", ["i", "love", "code", "palace"], required_words=["code", "palace"]
    )

    # Longer responses
    response(long.R_ADVICE, ["give", "advice"], required_words=["advice"])
    response(long.R_EATING, ["what", "you", "eat"], required_words=["you", "eat"])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    print(highest_prob_list)
    print(f"Best match = {best_match} | Score: {highest_prob_list[best_match]}")

    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


def filter_response(input: str):
    split_message = re.split(r"\s+|[,;?!.-]\s*", input.lower())
    response = check_all_messages(split_message)
    return response


def is_email_address(email: str):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def check_logged_user(telegram_id: str):
    # Request to redis
    pass


# Commands
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
        "/login <email> - Login to your account using email\n"
        "/custom - Show custom function message\n"
        "/echo <message> - Echo back the message you send"
    )
    await update.message.reply_text(help_text)


async def login_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id
    args = context.args

    # Check validity of arguments
    if not args:
        await update.message.reply_text(
            "You need to provide you registered email. Type /help to more details"
        )
        return

    email = args[0]
    if not is_email_address(email):
        await update.message.reply_text(f"The entered email address not valid!")

    # Send login email
    success = send_email(
        subject="Billy Telegram Login",
        body=placeholder_login_email(email, telegram_id),
        sender=EMAIL_ADDRESS,
        recipients=email,
        password=EMAIL_PASSWORD,
    )
    if success:
        await update.message.reply_text(
            f"Email sent successfully. You can click the link to login"
        )
    else:
        await update.message.reply_text(
            f"Email sending failed. Please try again later."
        )


async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        # List all wallets
        pass


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    await update.message.reply_text(f"The context echoing: {args}")


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
            response: str = handle_response(new_text)
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
    application.add_handler(CommandHandler("login", login_command))
    application.add_handler(CommandHandler("echo", echo_command))
    application.add_handler(CommandHandler("custom", custom_command))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    application.add_error_handler(error)

    # Run the bot
    print(f"Starting bot at {BOT_URL} with token {BOT_TOKEN}")
    print("Pooling...")
    application.run_polling(poll_interval=3)
