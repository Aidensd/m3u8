from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import subprocess

TOKEN = "6386389667:AAGCcROIr0WTYe6YdyUNMHeTPRe4rs4Yng0"

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def convert(update: Update, context: CallbackContext) -> None:
    link = context.args[0]
    name = context.args[1]
    encoding_choice = int(context.args[2])

    if encoding_choice == 1:
        command = f'ffmpeg -i {link} -c:v libaom-av1 -crf 25 -b:v 0 -strict experimental -tile-columns 4 -frame-parallel 1 -auto-alt-ref 1 -lag-in-frames 25 -c:a copy {name}.mkv'
    elif encoding_choice == 2:
        command = f'ffmpeg -i {link} -c:v libx265 -crf 25 -preset medium -c:a copy {name}.mkv'
    elif encoding_choice == 3:
        command = f'ffmpeg -i {link} -c:v libx264 -preset veryfast -crf 20 -c:a copy {name}.mkv'
    elif encoding_choice == 4:
        command = f'ffmpeg -i {link} -c copy -bsf:a aac_adtstoasc {name}.mkv'
    else:
        update.message.reply_text("Invalid encoding choice")
        return

    try:
        subprocess.run(command, shell=True, check=True)
        update.message.reply_text(f'{name}.mkv created successfully.')
    except subprocess.CalledProcessError as e:
        update.message.reply_text(f'An error occurred while converting "{link}" to "{name}.mkv". Error message: {str(e)}')

def main() -> None:
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("convert", convert))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
