from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
NAME, PHONE, MAIN_MENU, SETTINGS, ORDERS, PRODUCTS, SUPPORT, BACK_MENU, CART, PRODUCT1, MENU, CHANGE, \
CONTACT = range(13)


def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    update.message.bot.sendMessage(chat_id, text='Hi! My name is Test Bot.', reply_markup=ReplyKeyboardRemove())
    request_name(update, context)
    return NAME


def request_name(update, context):
    update.message.reply_text("What is your name?")
    return NAME


def get_name(update, context):
    name = update.message.text
    print(name)
    request_phone(update, context)
    return PHONE


def request_phone(update, context):
    buttons = [
        [KeyboardButton('My number', request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Now, send me your phone number 📞', reply_markup=reply_markup)
    return PHONE


def get_phone(update, context):
    phone = update.message.contact.phone_number
    update.message.reply_text("Great, now let's see the main menu")
    print(phone)
    main_menu(update, context)

    return MAIN_MENU


def main_menu(update, context):
    buttons1 = [
        [KeyboardButton('Order')],
        [KeyboardButton('Settings'), KeyboardButton('Support')],
        [KeyboardButton('Menu')]
    ]
    reply_markup1 = ReplyKeyboardMarkup(buttons1, resize_keyboard=True)
    update.message.reply_text('Main Menu: ', reply_markup=reply_markup1)

    return MAIN_MENU


def back_to_menu(update, context):
    main_menu(update, context)
    return MAIN_MENU


def orders(update, context):
    buttons = [
        [KeyboardButton('My cart')],
        [KeyboardButton('Back')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Orders is opened', reply_markup=reply_markup)
    return ORDERS


def cart(update, context):
    update.message.reply_text('This is what you have ordered so far:',
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      ['Back']
                                  ], resize_keyboard=True
                              ))
    return CART


def settings(update, context):
    buttons = [
        [KeyboardButton('Change')],
        [KeyboardButton('Back')]
    ]
    update.message.reply_text('Settings is opened',
                              reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return SETTINGS


def support(update, context):
    buttons = [
        [KeyboardButton('Contact')],
        [KeyboardButton('Back')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Support is opened', reply_markup=reply_markup)
    return SUPPORT


def contact(update, context):
    context.bot.send_contact(chat_id=update.message.chat_id,
                             phone_number='+998998789907',
                             first_name='Nuriddin', reply_markup=ReplyKeyboardMarkup(
            [
                ['Back']
            ], resize_keyboard=True
        ))
    return CONTACT


def change(update, context):
    update.message.reply_text('You changed something.',
                              reply_markup=ReplyKeyboardMarkup(
                                  [
                                      ['Back']
                                  ], resize_keyboard=True
                              ))
    return CHANGE


def menu(update, context):
    buttons = [
        [KeyboardButton('Product 1')],
        [KeyboardButton('Back')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    update.message.reply_text('Menu is opened', reply_markup=reply_markup)
    return MENU


def product_1(update, context):
    update.message.reply_text('Product 1 is chosen', reply_markup=ReplyKeyboardMarkup(
        [
            ['Back']
        ], resize_keyboard=True
    ))
    return PRODUCT1


def cancel(update, context):
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main():
    updater = Updater(token="1744385637:AAG7dJnNlOEtH2hT6xIKKOHOITOUtAUw23o")
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [
                MessageHandler(Filters.text, get_name)
            ],
            PHONE: [
                MessageHandler(Filters.contact, get_phone)
            ],
            MAIN_MENU: [
                MessageHandler(Filters.regex('Order'), orders),
                MessageHandler(Filters.regex('Settings'), settings),
                MessageHandler(Filters.regex('Support'), support),
                MessageHandler(Filters.regex('Menu'), menu)
            ],
            SETTINGS: [
                MessageHandler(Filters.regex('Change'), change),
                MessageHandler(Filters.regex('Back'), back_to_menu)
            ],
            ORDERS: [
                MessageHandler(Filters.regex('My cart'), cart),
                MessageHandler(Filters.regex('Back'), back_to_menu)
            ],
            CART: [
                MessageHandler(Filters.regex('Back'), orders)
            ],
            MENU: [
                MessageHandler(Filters.regex('Product 1'), product_1),
                MessageHandler(Filters.regex('Back'), back_to_menu)

            ],
            PRODUCT1: [
                MessageHandler(Filters.regex('Back'), menu)
            ],
            CHANGE: [
                MessageHandler(Filters.regex('Back'), settings)
            ],
            SUPPORT: [
                MessageHandler(Filters.regex('Contact'), contact),
                MessageHandler(Filters.regex('Back'), back_to_menu)
            ],
            CONTACT: [
                MessageHandler(Filters.regex('Back'), support)
            ]

        },
        fallbacks=[]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
