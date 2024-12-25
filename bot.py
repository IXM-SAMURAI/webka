import logging
import random
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ConversationHandler

# Включите логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Константы для хранения состояния разговора
DELAY = range(1)
PLAY_GAME = range(2)

# Определите функцию для обработки команды /start
def start(update: Update, context: ConversationHandler):
    update.message.reply_text('Привет! Давай сыграем в "Камень, ножницы, бумага". Выбери один из вариантов: камень, ножницы или бумага.')
    return PLAY_GAME

# Определите функцию для обработки команды /help
def help_command(update: Update, context: ConversationHandler):
    update.message.reply_text('Отправьте мне "камень", "ножницы" или "бумага", и я сделаю свой ход.')
    return PLAY_GAME

# Определите функцию для обработки текстовых сообщений
def play_game(update: Update, context: ConversationHandler):
    user_choice = update.message.text.lower()
    choices = ['камень', 'ножницы', 'бумага']

    if user_choice not in choices:
        update.message.reply_text('Пожалуйста, выберите "камень", "ножницы" или "бумага".')
        return DELAY

    bot_choice = random.choice(choices)
    update.message.reply_text(f'Я выбрал: {bot_choice}')

    if user_choice == bot_choice:
        update.message.reply_text('Ничья!')
    elif (user_choice == 'камень' and bot_choice == 'ножницы') or \
         (user_choice == 'ножницы' and bot_choice == 'бумага') or \
         (user_choice == 'бумага' and bot_choice == 'камень'):
        update.message.reply_text('Ты выиграл!')
    else:
        update.message.reply_text('Я выиграл!')

    return ConversationHandler.END

# Определите функцию для обработки ошибок
def error(update: Update, context: ConversationHandler):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Определите основной функционал бота
def main():
    # Вставьте сюда ваш токен API
    TOKEN = '7922042861:AAFgsnzm5Hwb5nyKHq_Z-MdpaCUm5Li0a5A'

    # Создайте экземпляр Updater
    updater = Updater(TOKEN, use_context=True)

    # Регистрируем обработчики
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))
    updater.dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, play_game))

    # Регистрируем обработчик ошибок
    updater.dispatcher.add_error_handler(error)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()