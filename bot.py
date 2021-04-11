import telegram
import logging
import json
from datetime import datetime
from config.config import tgToken, admins , adminChannel
from db.configuredb import DataBase
from config.elements import (
    first_button , 
    time , 
    guests , 
    hold , 
    phone_button,
    getTimeText,
    getGuestsText,
    getHolTimeText,
    getPhoneText,
    finishText,
    cancelText,
    )
from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update ,
    User,
    Contact
    )
from telegram.ext import (
    CallbackContext, 
    CommandHandler, 
    Updater, 
    MessageHandler , 
    Filters,
    ConversationHandler,
    )

#conversation methods
NAME , TIME , GUESTS , TIMETOHOLD , PHONE = range(5)

def start(update: Update , context : CallbackContext) -> int :
    reply_keyboard = first_button

    info = update.message.from_user
    name = info.first_name
    userId= info.id
    
    update.message.reply_text(
        f"Привет, {name}! Ты хочешь посетить нашу уютную кальянную?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    DataBase.createAction(userId, name = name)

    return NAME

def getTime(update: Update , context : CallbackContext) -> int :
    reply_keyboard = time

    update.message.reply_text(
        getTimeText,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),   
    )

    return TIME    

def getGuests(update: Update , context : CallbackContext) -> int :

    reply_keyboard = guests

    update.message.reply_text(
        getGuestsText,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),   
    )

    info = update.message.from_user
    userId= info.id
    
    funcName = "getGuests"
    reserveTime = update.message.text

    DataBase.updateAction(reserveTime, funcName=funcName , userId= userId)

    return GUESTS

def getHoldTime(update: Update , context : CallbackContext) -> int :

    reply_keyboard = hold

    update.message.reply_text(
        getHolTimeText,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),   
    )

    info = update.message.from_user
    userId= info.id
    
    funcName = "getHoldTime"
    guestsCount = update.message.text

    DataBase.updateAction(guestsCount, funcName=funcName , userId= userId)

    return TIMETOHOLD

def getPhone(update: Update , context : CallbackContext) -> int :

    reply_markups = telegram.ReplyKeyboardMarkup([[telegram.KeyboardButton(phone_button, request_contact=True)]])

    update.message.reply_text(
        getPhoneText,
        reply_markup= reply_markups,   
    )

    info = update.message.from_user
    userId= info.id
    
    funcName = "getPhone"
    longTime = update.message.text

    DataBase.updateAction(longTime, funcName=funcName , userId= userId)

    return PHONE

def finish(update: Update , context : CallbackContext) -> int :
    update.message.reply_text(finishText)  

    #getting info about user 
    contact = update.effective_message.contact
    phone = contact['phone_number']
    contact = update.effective_message.contact
    info = update.message.from_user
    name = info.first_name
    userId = info.id
    userInfo = DataBase.getLastActionByUser(userId)
    reserveTime = userInfo['reserveTime']
    guests = userInfo['guests']
    longTime = userInfo["longTime"]

    #send message in admin chat
    context.bot.send_message(
        chat_id = adminChannel,
        text= f'*Новая запись* \nИмя: {name} \nХочет придти в {reserveTime} \nКоличество гостей : {guests}  \nПросидят {longTime} \nНомер телефона: {phone}',
        parse_mode = telegram.ParseMode.MARKDOWN_V2
    )

    dbInfo = {
        "name" : name,
        "phone" : phone
    }


    DataBase.createUser(dbInfo, userId = userId)

    return ConversationHandler.END

def cancel(update: Update , context : CallbackContext) -> int :
    update.message.reply_text(cancelText)

    return ConversationHandler.END


def mailing(update: Update , context : CallbackContext) :
    info = update.message.from_user
    userId = info.id

    if str(userId) in admins :
        message = update.message.text

        users = DataBase.getUsersList(message)

        for user in users :
            context.bot.send_message(chat_id=user, text=message)
    
    else :
        pass

if __name__ == "__main__" :
    
    bot = telegram.Bot(token=tgToken)
    updater = Updater(token=tgToken, use_context=True)
    dispatcher = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points= [CommandHandler('start', start)],
        states= {
            NAME: [MessageHandler(Filters.text, getTime)], 
            TIME: [MessageHandler(Filters.text, getGuests)] , 
            GUESTS: [MessageHandler(Filters.text, getHoldTime)] , 
            TIMETOHOLD: [MessageHandler(Filters.text, getPhone)],
            PHONE: [MessageHandler(Filters.contact, finish)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    mailing_handler = MessageHandler(Filters.text, mailing)

    #test_handler= CommandHandler('test',test)
    #dispatcher.add_handler(test_handler)
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(mailing_handler)
    
    updater.start_polling()

    updater.idle()
