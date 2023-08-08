from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.error import TelegramError
from typing import List
import subprocess
import shlex
import logging
import os

TOKEN = "your-token-here"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
    Available commands:
    /start - Start the bot
    /convert <link> <output_name> <encoding_choice> - Convert a video
    Encoding choices:
    1 - AV1
    2 - H.265/HEVC
    3 - H.264/AVC
    4 - Copy existing encoding
    """
    update.message.reply_text(help_text)

def convert(update: Update, context: CallbackContext) -> None:
    """Convert a video."""
    # ... existing code ...

def handle_file(update: Update, context: CallbackContext) -> None:
    """Handle file messages."""
    file = update.message.document

    if not file.mime_type.startswith('video/'):
        update.message.reply_text('Please send a video file.')
        return

    input_file_name = file.file_id
    file.download(input_file_name)

    command = f'ffmpeg -i {input_file_name} -c:v libx265 -crf 25 -preset medium -c:a copy output.mkv'
    try:
        subprocess.run(command, shell=True, check=True)
        update.message.reply_text('output.mkv created successfully.')
        with open('output.mkv', 'rb') as video:
            context.bot.send_video(chat_id=update.effective_chat.id, video=video)
    except subprocess.CalledProcessError as e:
        logger.error(f'Error occurred: {str(e)}')
        update.message.reply_text(f'An error occurred while converting the video. Error message: {str(e)}')
    finally:
        if os.path.exists(input_file_name):
            os.remove(input_file_name)
        if os.path.exists('output.mkv'):
            os.remove('output.mkv')

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # ... existing code ...

def main() -> None:
    """Start the bot."""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("convert", convert))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("video/*"), handle_file))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
