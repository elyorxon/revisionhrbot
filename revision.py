import os
import logging

import re
import html
import json
import traceback
from telegram import ReplyKeyboardMarkup, Update, KeyboardButton
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

NAME, PHONE, LOCATION, AGE, WORKTYPE, STACK, EDUCATION, LANGUAGE, EXPERIENCE, PORTFOLIO, PURPOSE, WHY, CV = range(13)


def start(update, context):
    user_name = update.message.from_user.first_name
    update.message.reply_html(
        "Xush kelibsiz 😊. <b>'ReVision'</b> oilasiga qo’shilish niyatida kelgansiz"
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
    if re.match(andoza, phone_number):
        user = update.message.from_user

        places = [["Andijon viloyati", "Buxoro viloyati"],
                  ["Farg'ona viloyati", "Jizzax viloyati"],
                  ["Namangan viloyati", "Navoiy viloyati"],
                  ["Qashqadaryo viloyati", "Samarqand viloyati"],
                  ["Sirdaryo viloyati", "Surxondaryo viloyati"],
                  ["Toshkent viloyati", "Xorazm viloyati"],
                  ["Toshkent shahri", "Qoraqalpog'iston Respublikasi"]]
        reply_markup = ReplyKeyboardMarkup(places, resize_keyboard=True, one_time_keyboard=True)

        update.message.reply_html(
            '<b>{}</b>,🏢 hozirgi kunda qayerda istiqomat qilasiz? Tanlang👇:'.format(user.first_name),
            reply_markup=reply_markup
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Iltimos, to'g'ri formatdagi telefon raqam kiriting!",

        )
    return LOCATION



def get_location(update, context):

    context.user_data[LOCATION] = update.message.text
    age = [["<18", "18-25", "25<"]]
    reply_markup = ReplyKeyboardMarkup(age, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("Yosh oralig'ingizni tanlang!", reply_markup=reply_markup)

    return AGE


def get_age(update, context):
    context.user_data[AGE] = update.message.text
    worktype = [["Onlayn", "Ofisda", "Aralash"]]
    reply_markup = ReplyKeyboardMarkup(worktype, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("Qaysi ishlash uslubi siz uchun qulay?", reply_markup=reply_markup)

    return WORKTYPE


def get_worktype(update, context):
    context.user_data[WORKTYPE] = update.message.text
    stack = [["Back-End developer: Python, Django"],
             ["Front-End developer: React.Js"],
             ["Mobile developer: Java"],
             ["Back-End developer: C#, .NET"],
             ["Mobile developer: Flutter, Java"],
             ["Front-End developer: Vue.JS"]]
    reply_markup = ReplyKeyboardMarkup(stack, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_html("Siz qaysi  <b>yo'nalishda</b> ishlaysiz?",
                              reply_markup=reply_markup)

    return STACK


def get_stack(update, context):
    context.user_data[STACK] = update.message.text
    update.message.reply_html("Dasturlashni qayerda o'rgangansiz? Qaysi o'quv markazi yoki kurs? Yozib yuboring.")

    return EDUCATION

def get_education(update, context):
    context.user_data[EDUCATION] = update.message.text
    update.message.reply_html("Qaysi chet tilini qay darajada bilasiz? Misol uchun: English- B2 yoki bilmayman, shu formatda yozing.")
    return LANGUAGE


def get_language(update, context):
    context.user_data[LANGUAGE] = update.message.text
    experience = [["Tajribam yo'q"],
                  ["3-6 oy", "6 oy - 1 yil"],
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
    update.message.reply_html("Maqsadingiz nima? Qisqacha yozib yuboring.")
    return PURPOSE


def get_purpose(update, context):
    context.user_data[PURPOSE] = update.message.text

    update.message.reply_html(
        "<b>Nima uchun</b> aynan sizni ishga qabul qilishimiz kerak? Javobingizni yozib yuboring!")

    return WHY


def get_why_text(update, context):
    context.user_data[WHY] = update.message.text
    update.message.reply_html("<b>CV</b> hujjatingizni .pdf formatda jo'nating.")

    return CV


def get_cv(update, context):
    context.user_data[CV] = update.message.document.file_id
    update.message.reply_html(
        "Tashakkur. Sizning arizangiz qabul qilindi. Agar nomzodlar orasidan bizga ma'qul kelsangiz"
        " o'zimiz aloqaga chiqamiz.")

#
# def send_document_to_the_group(update, context):
    user = update.effective_user
    talabgor = f'''\n\n👤Nomzod ismi: {user.first_name, user.last_name}
                          \n👤Ismi: {context.user_data[NAME]}
                          \n📞Telefon raqami: {context.user_data[PHONE]}
                          \n🗺Yashash manzili: {context.user_data[LOCATION]}
                          \n📅Yosh toifasi: {context.user_data[AGE]}
                          \n🏢Ishlash turi: {context.user_data[WORKTYPE]}
                          \n👨🏻‍💻Stack: {context.user_data[STACK]}
                          \n🎓 Ma'lumoti:  {context.user_data[EDUCATION]}
                          \n🇺🇸Chet tili:  {context.user_data[LANGUAGE]}
                           \n💼Ish tajribasi:  {context.user_data[EXPERIENCE]}
                           \n🔗Portfolio: {context.user_data[PORTFOLIO]}
                           \n📈Maqsadi: {context.user_data[PURPOSE]}
                          \n🙋🏻‍♂️Nima uchun: {context.user_data[WHY]}
                          \n 👤Nomzod havolasi: {user.link, user.full_name}
                              '''
    file_id = update.message.document.file_id
    context.bot.send_document(chat_id=50646151, document=file_id, caption=talabgor)

#-978933128


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
            PHONE: [MessageHandler(Filters.text | Filters.contact, get_phone, pass_user_data=True)],
            LOCATION: [MessageHandler(Filters.regex("^(Andijon viloyati|Buxoro viloyati|Farg'ona viloyati|"
                                                    'Jizzax viloyati|Namangan viloyati|Navoiy viloyati|'
                                                    'Qashqadaryo viloyati|Samarqand viloyati|Sirdaryo viloyati|'
                                                    'Surxondaryo viloyati|Toshkent viloyati|Xorazm viloyati|'
                                                    'Toshkent shahri|Qoraqalpog\'iston Respublikasi)$'),
                                      get_location, pass_user_data=True)],
            AGE: [MessageHandler(Filters.regex('^(<18|18-25|25<)$'), get_age, pass_user_data=True)],
            WORKTYPE: [MessageHandler(Filters.regex("^(Onlayn|Ofisda|Aralash)$"), get_worktype, pass_user_data=True)],
            STACK: [MessageHandler(Filters.regex('^(Back-End developer: Python, Django|Front-End developer: React.Js|'
                                                 'Mobile developer: Flutter, Java|Back-End developer: C#, .NET|'
                                                 'Front-End developer: Vue.JS|Mobile developer: Java)$'), get_stack, pass_user_data=True)],
            EDUCATION: [MessageHandler(Filters.text, get_education, pass_user_data=True)],
            LANGUAGE: [MessageHandler(Filters.text, get_language, pass_user_data=True)],
            EXPERIENCE: [MessageHandler(Filters.regex('^(Tajribam yo\'q|3-6 oy|6 oy - 1 yil|1 - 2 yil|2 yildan ko\'proq)$'), get_experience, pass_user_data=True)],
            PORTFOLIO: [MessageHandler(Filters.text, get_portfolio, pass_user_data=True)],
            PURPOSE: [MessageHandler(Filters.text, get_purpose, pass_user_data=True)],
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




