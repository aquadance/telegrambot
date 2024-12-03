import os
import logging
import yt_dlp

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логов: DEBUG для максимальной информации
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot.log",  # Логи будут записываться в файл bot.log
    filemode="a"  # Логи добавляются в файл, а не перезаписываются
)

# Папка для загрузки файлов
DOWNLOAD_DIR = "downloads"

# Убедимся, что папка загрузки существует
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_song(song_name: str) -> str:
    """
    Ищет и скачивает песню по названию с YouTube.
    Возвращает путь к MP3-файлу или None, если произошла ошибка.
    """
    logging.info(f"Запрос на загрузку песни: {song_name}")

    # Поисковый запрос для YouTube
    search_query = f"{song_name} audio"

    # Настройки yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,  # Показывать процесс загрузки
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Указываем путь к FFmpeg
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Ищем: {search_query}")
            
            # Выполняем поиск
            info = ydl.extract_info(f"ytsearch:{search_query}", download=False)
            logging.debug(f"Результаты поиска: {info}")

            if 'entries' in info and len(info['entries']) > 0:
                # Берем первый результат из поиска
                first_result = info['entries'][0]
                logging.info(f"Найден результат: {first_result['title']}")

                # Скачиваем файл
                ydl.download([first_result['webpage_url']])

                # Возвращаем путь к файлу
                file_path = ydl.prepare_filename(first_result).replace(".webm", ".mp3").replace(".m4a", ".mp3")
                logging.info(f"Файл загружен: {file_path}")
                return file_path
            else:
                logging.warning("Ничего не найдено")
                return None

    except Exception as e:
        logging.error(f"Ошибка загрузки: {e}")
        return None
