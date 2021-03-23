#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
import logging, telegram
from ai import codegenerator, dbconnect

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)

# Stages - States - Group of handlers to be active 
CHECKCODE, RETRYCODE, SECOND = range(3)
# Callback data
ONE, END, RETRY, CANCEL = range(4)

bot = telegram.Bot("936401514:AAEqcrYA_IFdzSEWRZhNN42Wo5RBVvhVUms")

def start(update, context):
    chat_type = update.message.chat.type
    starter = update.message.from_user.first_name
    starter_id = update.message.from_user.id

    if chat_type == 'private':
        db_conn = dbconnect()
        is_member = db_conn.ismemberbyid(starter_id)
        if is_member:
            update.message.reply_text('Hi {}! You are an existing member! .....Send menu for existing'.format(starter))
            return SECOND
        else: # not found in members database, then is a joiner ****also check joiner database for pending membership
            update.message.reply_text(
                'Welcome {}! Please enter your one-time referral code:'.format(starter),
                force_reply = True,
                selective = True,
                )
            logger.info(update.message)
            return CHECKCODE
        db_conn.closedbconnection()
    else:
        pass

def start_over(update, context):
    query = update.callback_query
    bot = context.bot
    chat_type = query.message.chat.type
    starter = query.from_user.first_name
    starter_id = query.from_user.id

    if chat_type == 'private':
        db_conn = dbconnect()
        is_member = db_conn.ismemberbyid(starter_id)
        if is_member:
            update.message.reply_text('Hi {}! You are an existing member! .....Send menu for existing'.format(starter))
            return SECOND
        else: # not found in members database, then is a joiner ****also check joiner database for pending membership
            bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                text= 'Welcome {}! Please enter your one-time referral code:'.format(starter),
                force_reply = True,
                selective = True,
                )
            logger.info(update.message)
            return CHECKCODE
        db_conn.closedbconnection()
    else:
        pass


def validate_refcode(update, context):
    refcode = update.message.text
    print(update.message.text)
    if refcode == '12345':
        bot.send_message(chat_id=update.message.chat_id, 
            text='VALID REFCODE!!!')

    else:
        # bot.send_message(chat_id=update.message.chat_id, text='INVALID REFCODE!!!')
        retry_option(update, context)
        return RETRYCODE
    # logger.info(update.message)


def retry_option(update, context):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("RETRY?", callback_data=str(RETRY)),
         InlineKeyboardButton("END", callback_data=str(END))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id= update.message.chat_id, 
        text= "INVALID CODE", 
        reply_markup= reply_markup)
    return CHECKCODE


def end(update, context):
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="See you next time!"
    )
    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():

    # Create the Updater and pass it your bot's token.
    updater = Updater("936401514:AAEqcrYA_IFdzSEWRZhNN42Wo5RBVvhVUms", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueryies with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHECKCODE: [MessageHandler(Filters.text, validate_refcode),
                    # CallbackQueryHandler(two, pattern='^' + str(RETRY) + '$'),
                    # CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
                    # CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$')
                    ],
            RETRYCODE: [CallbackQueryHandler(start_over, pattern='^' + str(RETRY) + '$'),
                        CallbackQueryHandler(end, pattern='^' + str(END) + '$')
                        ],
            SECOND: [CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
                     CallbackQueryHandler(end, pattern='^' + str(END) + '$')]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    # Add conversationhandler to dispatcher it will be used for handling
    # updates
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
