# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import src.config as config

TOKEN = config.token

knownUsers = []  # todo: save these in a file,
scheduleIDs = {}
userStep = {}  # so they won't reset every time the bot restarts

commands = {  # command description used in the "help" command
    'start': 'Get used to the bot',
    'help': 'Gives you information about the available commands',
    'sendLongText': 'A test using the \'send_chat_action\' command',
    'getSchedule': 'A test using multi-stage messages, custom keyboard, and media sending'
}


def init_keyboard(keyboard, buttons):
    for button in buttons:
        keyboard.add(button)

SID = 'SID'
GRADE = 'grade'
FACULTIES = 'faculties'
SPECIALITIES = 'speciality'
REQUIRED_SUBJECTS = 'requiredSubjects'
OPTIONAL_SUBJECTS = 'optionalSubjects'
BOK = 'BOK'

grades = ['Baccalaureate', 'Magistracy', 'Diploma']
faculties = ['Technical', 'Economic', 'Medical', 'Law', 'Math and Physics', 'Chemistry', 'Philological']
specialities = ['BWL and economics', 'Shit', 'Another shit']
requiredSubjects = ['Physical culture', 'History', 'Microeconomics']
optionalSubjects = ['Law', 'Physics', 'Kek']
BOK = ['Straight', 'Gay', 'Lesbian']

gradeKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
init_keyboard(gradeKeyboard, grades)

facultiesKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
init_keyboard(facultiesKeyboard, faculties)

specialityKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
init_keyboard(specialityKeyboard, specialities)

requiredSubjectsKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
init_keyboard(requiredSubjectsKeyboard, requiredSubjects)

optionalSubjectsKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
init_keyboard(optionalSubjectsKeyboard, optionalSubjects)

BOKKeyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
init_keyboard(BOKKeyboard, BOK)

imageSelect = types.ReplyKeyboardMarkup(one_time_keyboard=True)  # create the image selection keyboard
imageSelect.add('cock', 'pussy')

hideBoard = types.ReplyKeyboardHide()  # if sent as reply_markup, will hide the keyboard


# error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
def get_user_step(uid):
    if uid in scheduleIDs.keys():
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = SID
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if cid not in knownUsers:  # if user hasn't used the "/start" command yet:
        knownUsers.append(cid)  # save user id, so you could brodcast messages to all users of this bot later
        userStep[cid] = SID
        bot.send_message(cid, "Hello, student, let me remember you...")
        bot.send_message(cid, "Remembering complete, I know everything about you now")
        bot.send_message(cid, "MWA-HA-HA")
        bot.send_message(cid, "I'm joking, sorry")
        bot.send_message(cid, "Now, please give me your eight-digit ID!")
        # command_help(m)  # show the new user the help page
    else:
        bot.send_message(cid, "I already know you, no need to remember you again!")


# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page


# chat_action example (not a good one...)
@bot.message_handler(commands=['sendLongText'])
def command_long_text(m):
    cid = m.chat.id
    bot.send_message(cid, "If you think so...")
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(3)
    bot.send_message(cid, ".")


@bot.message_handler(commands=['getSchedule'])
def command_get_schedule(m):
    cid = m.chat.id
    if get_user_step(cid) == SID:
        bot.send_message(cid, "Please, give me your eight-digit ID")
    else:
        bot.send_message(cid, "Please, choose variants", reply_markup=gradeKeyboard)  # show the keyboard


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == GRADE)
def msg_grade_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Please, choose variants", reply_markup=facultiesKeyboard)  # show the keyboard
    userStep[cid] = FACULTIES  # set the user to the next step (expecting a reply in the listener now)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == FACULTIES)
def msg_faculty_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Please, choose variants", reply_markup=specialityKeyboard)  # show the keyboard
    userStep[cid] = SPECIALITIES  # set the user to the next step (expecting a reply in the listener now)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == SPECIALITIES)
def msg_speciality_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Please, choose variants", reply_markup=requiredSubjectsKeyboard)  # show the keyboard
    userStep[cid] = REQUIRED_SUBJECTS  # set the user to the next step (expecting a reply in the listener now)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == REQUIRED_SUBJECTS)
def msg_required_subjects_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Please, choose variants", reply_markup=optionalSubjectsKeyboard)  # show the keyboard
    userStep[cid] = OPTIONAL_SUBJECTS  # set the user to the next step (expecting a reply in the listener now)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == OPTIONAL_SUBJECTS)
def msg_optional_subjects_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Please, choose variants", reply_markup=BOKKeyboard)  # show the keyboard
    userStep[cid] = BOK  # set the user to the next step (expecting a reply in the listener now)


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == BOK)
def msg_bok_select(m):
    cid = m.chat.id
    bot.send_message(cid, "Congratulations, comrade! Here is your schedule", reply_markup=hideBoard)
    bot.send_message(cid, "None...")
    userStep[cid] = GRADE  # set the user to the next step (expecting a reply in the listener now)


# filter on a specific message
@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'], regexp='^\d{8}$')
def command_text_sid(m):
    # this is the standard reply to a normal message
    scheduleIDs[m.chat.id] = m.text
    userStep[m.chat.id] = GRADE
    bot.send_message(m.chat.id, "Thank you!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    if m.chat.id in knownUsers:
        if userStep[m.chat.id] == SID:
            bot.send_message(m.chat.id, "I told you to give me an eight-digit ID!")
    else:
        bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")


bot.polling()
