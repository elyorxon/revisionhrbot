import os
import logging
import datetime as dt
import re
import html
import json
import traceback
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
DEVELOPER_CHAT_ID = 1287282005


def error_handler(update, context):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        'An exception was raised while handling an update\n'
        '<pre>update = {}</pre>\n\n'
        '<pre>context.chat_data = {}</pre>\n\n'
        '<pre>context.user_data = {}</pre>\n\n'
        '<pre>{}</pre>'
    ).format(
        html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False)),
        html.escape(str(context.chat_data)),
        html.escape(str(context.user_data)),
        html.escape(tb)
    )
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode='html')


PORT = int(os.environ.get('PORT', '8443'))
TOKEN = "6156512482:AAFnQCPRbKFNCyFO3yHqFn32qPpt-MzrOtQ"

NAME, PHONE, PLACE, AGE, STACK, EXPERIENCE, PORTFOLIO, PURPOSE, WHY, CV = range(10)


def start(update, context):
    user_name = update.message.from_user.first_name
    update.message.reply_html(
        "Xush kelibsiz 😊. 'ReVision' oilasiga qo’shilish niyatida kelgansiz"
        " degan umiddamiz. Iltimos ariza muvafaqqiyatli yakun topishi uchun so’ralgan "
        " barcha ma’lumotlarni oxirigacha va to’g’ri kiriting. Birinchi navbatda familya va ismingizni yozib "
        " jo'nating. "
        .format(user_name))

    return NAME


def get_name(update, context):
    """ Get the name of user """
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    context.user_data[NAME] = update.message.text
    contact_keyboard = KeyboardButton(text="📞Telefon raqam ulashish", request_contact=True)
    custom_keyboard = [[contact_keyboard]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html(
        "Ajoyib 🤩 Siz bilan aloqaga chiqishimiz uchun telefon raqamingizni yozib qoldiring (+998xx-xxx-xx),"
        " yoki pastdagi tugmacha ustiga bosib telefon raqamingizni tasdiqlang 😊 ".format(user.first_name),
        reply_markup=reply_markup
    )
    return PHONE

def get_phone(update, context):
    context.user_data[PHONE] = update.message.text or update.effective_message.contact.phone_number
    logger.info("Phone number of %s: %s", update.message.text)

    andoza = '^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'
    phone_number = context.user_data[PHONE]

    keyboards = [["Toshkent shahri", "Andijon", "Buxoro"],
                 ["Farg'ona", "Jizzax", "Namangan"],
                 ["Navoiy", "Samarqand", "Sirdaryo"],
                 ["Surxandaryo", "Qashqadaryo", "Toshkent viloyati"],
                 ["Qoraqalpog'iston Respublikasi", "Xorazm"]]
    places = ReplyKeyboardMarkup(keyboards, resize_keyboard=True)

    context.user_data[NAME] = update.message.text
    age = [["<18", "18-25", "25<"]]
    reply_markup = ReplyKeyboardMarkup(age, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("Yosh oralig'ingizni tanlang!", reply_markup=reply_markup)

    return AGE


def get_age(update, context):
    context.user_data[AGE] = update.message.text
    stack = [["Back-End developer: Python, Django"],
             ["Front-End developer: React.Js"],
             ["Mobile developer: Java"],
             ["Back-End developer: C#, .NET"],
             ["Mobile developer: Flutter, Java"],
             ["Front-End developer: Vue.JS"]]
    reply_markup = ReplyKeyboardMarkup(stack, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("O'zingiz ustozlik qilmoqchi bo'lgan <b>yo'nalishni</b> tanlang!",
                              reply_markup=reply_markup)

    return STACK


def get_stack(update, context):
    context.user_data[STACK] = update.message.text
    experience = [["0-6 oy", "6 oy - 1 yil"],
                  ["1 - 2 yil", "2 yildan ko'proq"]]
    reply_markup = ReplyKeyboardMarkup(experience, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("Tijoriy loyihalarda <b>ish tajribangiz</b> qancha?", reply_markup=reply_markup)

    return EXPERIENCE


def get_experience(update, context):
    context.user_data[EXPERIENCE] = update.message.text
    update.message.reply_html("Qilgan ishlaringiz havolasini yoki github havolasini jo'nating!")

    return PORTFOLIO


def get_portfolio(update, context):
    context.user_data[PORTFOLIO] = update.message.text
    pray = [["✅Ha", "❌Yo'q"]]
    reply_markup = ReplyKeyboardMarkup(pray, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("Namoz o'qiysizmi?", reply_markup=reply_markup)
    return PRAY




def get_pray(update, context):
    context.user_data[PRAY] = update.message.text
    update.message.reply_html(
        "<b>Nima uchun</b> aynan sizni ishga qabul qilishimiz kerak? Javobingizni yozib yuboring!")

    return WHY


def get_why_text(update, context):
    context.user_data[WHY] = update.message.text
    update.message.reply_html("<b>CV</b> hujjatingizni .pdf formatda jo'nating.")

    return CV


def get_cv(update, context):
    context.user_data[CV] = update.message.document.file_id
    now = dt.datetime.now()
    user = update.effective_user
    file_id = update.message.document.file_id
    context.bot.send_document(chat_id=-876750276, document=file_id)
    date_time = now.strftime("%m/%d/%Y, %H:%M")
    talabgor = f'''\n\n👤Nomzod ismi: {user.first_name, user.last_name}
                       \n👤Ismi: {context.user_data[NAME]}
                       \n📅Yosh toifasi: {context.user_data[AGE]}
                       \nStack: {context.user_data[STACK]} 
                       \nTajribasi: {context.user_data[EXPERIENCE]} 
                       \nWhy: {context.user_data[WHY]}
                       \nPray: {context.user_data[PRAY]}
                       \nPortfolio: {context.user_data[PORTFOLIO]}
                       \n📆 Hujjat jo'natilgan vaqt: {date_time}
                       \n 👤Nomzod havolasi: {user.link, user.full_name}
                           '''
    context.bot.send_message(chat_id=-876750276,
                             text=talabgor,
                             parse_mode='HTML'
                             )

    update.message.reply_html(
        "Tashakkur. Sizning arizangiz qabul qilindi. Agar nomzodlar orasidan bizga ma'qul kelsangiz"
        " o'zimiz aloqaga chiqamiz.")


    return ConversationHandler.END



def cancel(update: Update, context: CallbackContext):
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_html(
        "🇺🇿{}, sog'-salomat bo'ling. Bizning botdan foydalanganingizdan xursandmiz."
        "Anketani boshqattan to'ldirish uchun /start buyrug'ini bosing!"
        "Agar sizda qo'shimcha savollar bo'lsa javob berishdan mamnunmiz.\n\n"
        "🇷🇺 Быть здоровым Рад, что вы воспользовались нашим ботом. Нажмите команду /start, чтобы заполнить форму! Мы будем"
        " рады ответить на любые дополнительные вопросы, которые могут у вас возникнуть.".format(user.first_name)
    )

    return ConversationHandler.END


def main():
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, run_async=True)],
        states={
            NAME: [MessageHandler(Filters.text, get_name, pass_user_data=True)],
            AGE: [MessageHandler(Filters.regex('^(<18|18-25|25<)$'), get_age, pass_user_data=True)],
            STACK: [MessageHandler(Filters.regex('^(Back-End developer: Python, Django|Front-End developer: React.Js|'
                                                 'Mobile developer: Flutter, Java|Back-End developer: C#, .NET|'
                                                 'Front-End developer: Vue.JS|Mobile developer: Java)$'), get_stack, pass_user_data=True)],
            EXPERIENCE: [MessageHandler(Filters.regex('^(0-6 oy|6 oy - 1 yil|1 - 2 yil|2 yildan ko\'proq)$'), get_experience, pass_user_data=True)],
            PORTFOLIO: [MessageHandler(Filters.text, get_portfolio, pass_user_data=True)],
            PRAY: [MessageHandler(Filters.regex('^(✅Ha|❌Yo\'q)$'), get_pray, pass_user_data=True)],
            WHY: [MessageHandler(Filters.text, get_why_text, pass_user_data=True)],
            CV: [MessageHandler(Filters.document, get_cv, pass_user_data=True)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
        allow_reentry=True,
        run_async=True
    )
    dispatcher.add_handler(conv_handler)
    dispatcher.add_error_handler(error_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()




