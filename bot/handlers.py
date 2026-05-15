"""Telegram update handlers."""
import requests
from bs4 import BeautifulSoup
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import html5lib

logger = logging.getLogger(__name__)

#Настройка парсинга сайта
# driver = webdriver.Chrome()
# driver.get('https://ibc.mirea.ru/')
s = requests.Session()
mirea_url = 'https://ibc.mirea.ru/books/search/?search_field='
s.headers.update({'Referer': mirea_url})
# csrf = form.find('input', {'name': 'csrfmiddlewaretoken'}).get('value')

#Настройка парсинга сайта

BOT_COMMANDS = (
    ("start", "Show the main menu"),
    ("pars", "Show help"),
    ("test", "Show help")
)

MENU_HELP = "Help"
MENU_ABOUT = "About"
MENU_PING = "Ping"
global Glob_Message
MAIN_MENU_KEYBOARD = ReplyKeyboardMarkup(
    [[MENU_HELP, MENU_ABOUT], [MENU_PING]],
    resize_keyboard=True,
    is_persistent=True,
    input_field_placeholder="Choose a menu item",
)

HELP_TEXT = """Available commands:
/start - Start the bot
/help - Show help
/about - Show bot information
/ping - Check bot status

Send a normal text message and the bot will echo it back."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    message = update.effective_message
    user = update.effective_user
    if message is None:
        return

    name = user.first_name if user and user.first_name else "friend"
    await message.reply_text(
        f"Привет, {name}! Пупупум тестик.\n\n"
        "Choose a menu button below or type /help to see the available commands.",
        reply_markup=MAIN_MENU_KEYBOARD,
    )



# async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     del context
#     message = update.effective_message
#     if message is None:
#         return
#
#     await message.reply_text(HELP_TEXT)

# async def pars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     del context
#     Glob_Message = update.effective_message
#     message = update.effective_message
#     print(message.text)
#     await message.reply_text("Сделайте запрос")
#     mess = Glob_Message
#     while "подтвердить" not in message.text:
#         time.sleep(1)
#
#         print(Glob_Message.text)
#         if Glob_Message.text != mess.text:
#             message = update.effective_message
#             await message.reply_text("Запрос: "+message.text+" подтвердить ?")
#             mess = Glob_Message
#
#     bibl_request = message.text






async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    message = update.effective_message
    user = update.effective_user
    if user.id in [8293418325]:
        print(message)
        # if message is None or not message.text:
        #     return

        await message.reply_text(f"Отправил:\n{message.text}")
        # Данные для запроса
        request_data = {
            'search_field': message.text
        }
        # Отправляем форму
        # form = driver.find_element(By.CLASS_NAME, 'main__search-form')
        # input_field = form.find_element(By.TAG_NAME, 'input')
        # input_field.send_keys(message.text)
        # # Отправляем форму
        # form.submit()
        soup = BeautifulSoup(s.get(mirea_url + message.text).text, 'html.parser')

        # response = s.post(form.get('action'), { 'search_field': message.text})
        # print(soup)
        for i in soup.find_all(class_="bib-desc"):
            m = ""
            print(i.text)
            book = [j for j in BeautifulSoup(i.text, 'html5lib')]
            for j in book:
                j = j.text
                [j := j.replace(st, " ") for st in [".—", "/", ": "]]
                m += "-------------\n" + j
            print(book)
            await message.reply_text(f"Результат:\n{m}")
        return 0
    else:
        await message.reply_text(f"Айди не одобрен:\n{user.id}")

        return 0




async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    del context
    message = update.effective_message
    if message is None:
        return

    await message.reply_text("Unknown command. Type /help for assistance.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Error while processing update: %s", update, exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Sorry, an error occurred while processing your message."
        )


async def set_bot_commands(application: Application) -> None:
    await application.bot.set_my_commands(BOT_COMMANDS)


def register_handlers(application: Application) -> None:
    application.add_handler(CommandHandler("start", start))
    # application.add_handler(CommandHandler("pars", pars))
        # application.add_handler(CommandHandler("test", test))
    # application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_handler(
        MessageHandler(filters.TEXT, echo)
    )
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
