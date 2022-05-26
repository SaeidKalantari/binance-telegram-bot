import logging
import io
from binance import Client
import datetime
from matplotlib import pyplot as plt
import pandas as pd
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler, CallbackContext)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def get_btc_usdt(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""

    # OUR KEYS
    api_key = 'Binance_API_Key'
    api_secret = 'Binance_Secret_Key'
    client = Client(api_key, api_secret)

    # TWO FUNCTIONS TO MANAGE THE DATE
    def unix_to_datetime(unix_time):
        return datetime.datetime.fromtimestamp(unix_time / 1000.0)

    def date_to_unix(date):
        date = datetime.datetime.now()
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date = date - datetime.timedelta(days=7)
        return int(date.timestamp() * 1000)

    # THE CRYPTO WE ARE GOING TO TRACK
    crypto = 'BTCUSDT'

    # RETRIEVE THE DATA FROM THE API
    klines = client.get_historical_klines(crypto, Client.KLINE_INTERVAL_5MINUTE, date_to_unix(datetime.datetime.now()))
    values = [[unix_to_datetime(el[0]), float(el[1])] for el in klines]
    df = pd.DataFrame(values, columns=['ds', 'y'])
    plt.plot(df['ds'], df['y'])
    plt.xticks(rotation=15)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    update.message.reply_photo(img)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("Telegram-API-Key")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("btc", get_btc_usdt))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()