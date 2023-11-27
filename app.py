import logging
from task import *
from telegram import Update
from telegram.ext import CommandHandler,CallbackContext,Updater , MessageHandler,Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN = os.getenv("API_TOKEN")
ADMIN = int(os.getenv("ADMIN"))


def start(update: Update,context: CallbackContext):
    update.message.reply_text("Hello Send Me Instagram Reel Link Plox")

def s(reel_link: str, user_id: int, context: CallbackContext):
    edit_msg = context.bot.send_message(chat_id=user_id, text="Processing...")


    
    try:
        result = find_reel_downloadable_url(find_media_id(reel_link))

        if extract_scene(result) == 1:
            with open("output.jpg", 'rb') as image_file:

                # send_msg(result)
                context.bot.send_message(chat_id=ADMIN, text="Reels Link",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Click Here", url=result)]]))
                send_image()

                context.bot.editMessageText(message_id=edit_msg.message_id, chat_id=user_id, text="Reels Link",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Click Here", url=result)]]))
                context.bot.send_photo(chat_id=user_id, photo=image_file)
                context.bot.send_message(chat_id=user_id, text="Join Channel to see DUMPS",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Click Here", url="https://t.me/+XHs4qrlOvSE0MzIx")]]))

        else:
            context.bot.editMessageText(message_id=edit_msg.message_id, chat_id=user_id, text="Reels Link",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Click Here", url=result)]]))
            context.bot.send_message(message_id=edit_msg.message_id, chat_id=user_id, text="Not found KLPD")

    except Exception as e:
        print(e)
        context.bot.editMessageText(message_id=edit_msg.message_id, chat_id=user_id, text="Invalid Reels Link")
    

def process_message(update: Update, context: CallbackContext):
    reel_link = update.message.text
    user_id = update.message.chat_id
    s(reel_link, user_id, context)

    
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, process_message))

    #handlers from dispatcher
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("s", s))
    #   scrape.send_message(1800)

    #Start Polling and wait for any signal to end the program
    logger.info("Started Polling...")
    updater.start_polling()
    updater.idle()


main()
