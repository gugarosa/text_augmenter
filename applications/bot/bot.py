import configparser

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)


def start(update, context):
    """Handles the start command.

    Args:
        update (Update): An update object, basically holding vital information from a new user interaction.
        context (CallbackContext): A context object, if additional information is needed.

    """

    # Gathers user's first name
    first_name = update.message.chat.first_name

    print(f'New interaction from: {first_name}')

    # Sends back a reply
    update.message.reply_text(f'Olá, {first_name}! Por favor, me envie um texto inicial.')

    print(f'Awaiting response ...')

    return 'GENERATE'


def generate(update, context):
    """Handles the text generation.

    Args:
        update (Update): An update object, basically holding vital information from a new user interaction.
        context (CallbackContext): A context object, if additional information is needed.

    """

    # Gathers the input text
    input_text = update.message.text

    print(f'Generating text from: {input_text}')

    # Sends back the generated text
    update.message.reply_html(f'<b>{input_text}</b>')

    # Sends back the generated text
    update.message.reply_html(f'Caso queira gerar outro texto, por favor fale novamente comigo.')

    return ConversationHandler.END


def init(key):
    """Main process to initiate a customized bot needs.

    Args:
        key (str): A string holding the Telegram's API bot key.

    """

    print(f'Initializing the bot ...')

    # Initializing base class with Bot's token
    updater = Updater(key, use_context=True)

    # Getting the dispatcher to attach new handlers
    dp = updater.dispatcher

    # Add conversation handler to handle bot's states
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
                MessageHandler(Filters.regex('^(?i)(Ei|Olá|Ola|Oi|Bot)'), start)
            ],
            states={
                'GENERATE': [MessageHandler(Filters.text, generate)]
            },
            fallbacks=[
            ]
        )
    )

    # Actually start the polling of new updates
    updater.start_polling()

    # Used to handle its idle state
    updater.idle()


if __name__ == '__main__':
    # Initalizes the configuration object
    config = configparser.ConfigParser()

    # Parses a new config and get the bot's key
    config.read('config.ini')
    key = config.get('BOT', 'TELEGRAM_KEY')

    # Initializes the bot
    init(key)
