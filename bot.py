import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from music_fetcher import download_song

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot.log",
    filemode="a"
)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Пользователь запустил бота.")
    await update.message.reply_text(
        "Напиши /song <название>.\nПример: /song Imagine Dragons Believer"
    )

# Команда для поиска и отправки песни
async def get_song(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        logging.warning("Пользователь не ввел название песни.")
        await update.message.reply_text("Пожалуйста, укажите название песни. Пример: /song Imagine Dragons Believer")
        return

    song_name = " ".join(context.args)
    logging.info(f"Запрос от пользователя: {song_name}")
    await update.message.reply_text(f"Ищу и загружаю песню: {song_name}...")

    mp3_path = download_song(song_name)

    if mp3_path and os.path.exists(mp3_path):
        logging.info(f"Песня найдена и отправлена: {mp3_path}")
        await update.message.reply_text(f"Песня '{song_name}' найдена и загружена. Отправляю файл...")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(mp3_path, 'rb'))
        os.remove(mp3_path)
        logging.debug(f"Файл удален: {mp3_path}")
    else:
        logging.error(f"Песня '{song_name}' не найдена или произошла ошибка.")
        await update.message.reply_text(f"К сожалению, песня '{song_name}' не найдена.")

# Основная функция запуска бота
def main():
    logging.info("Запуск бота...")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", get_song))

    logging.info("Бот запущен и готов к работе.")
    app.run_polling()

if __name__ == "__main__":
    main()
