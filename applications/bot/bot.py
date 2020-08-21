import configparser

import json

import requests

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)


def generate_text(seed):
    """Performs a call to Google's API to perform speech-to-text.

    Args:
        audio_path (str): Path to audio that needs to be transcripted.

    Returns:
        An already decoded JSON object holding the desired innformation.

    """

    # Data structure
    data = {
        'seed': seed
    }

    # Dumping the data into a JSON object
    payload = json.dumps(data)

    # Tries to perform the API call
    try:
        # POST request over the part-of-speech API method
        r = requests.post('http://localhost:8080', data=payload)

        # Decoding response
        response = json.loads(r.text)

        # Accessing JSON object and gathering request's response
        result = response['result']

        return result

    # If by any chance it fails
    except:
        # Return the response as none
        return None


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
    update.message.reply_text(f'Hello, {first_name}! Please, send me a seed text.')

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

    update.message.reply_text('Please wait while I am generating the text ...')

    # Makes an API call to generate text
    text = generate_text(input_text + " ")

    # Sends back the generated text
    update.message.reply_text(text)

    # Sends back the generated text
    update.message.reply_html(f'If you wish to generate more text, please call me again.')

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
                MessageHandler(Filters.regex('^(?i)(Hey|Hello|Hi|Hallo|Bot)'), start)
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
