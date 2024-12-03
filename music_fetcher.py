import os
import yt_dlp
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot.log",
    filemode="a"
)

DOWNLOAD_DIR = "downloads"

# Укажите путь к ffmpeg
# Замените на полный путь к директории с `ffmpeg` и `ffprobe`
FFMPEG_PATH = "C:/ffmpeg-7.1-full_build/bin/ffmpeg.exe"  # Например, для Windows
FFPROBE_PATH = "C:/ffmpeg-7.1-full_build/bin/ffprobe.exe"  # Обычно находится в той же директории, что и ffmpeg

def download_song(song_name: str) -> str:
    """
    Ищет и скачивает песню по названию с YouTube.
    Возвращает путь к MP3-файлу.
    """
    logging.info(f"Запрос на загрузку песни: {song_name}")

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)
        logging.debug(f"Создана директория для загрузки: {DOWNLOAD_DIR}")
    
    search_query = f"{song_name} audio"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
        'ffmpeg_location': FFMPEG_PATH  # Указание пути к ffmpeg
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.debug(f"Ищем: {search_query}")
            info = ydl.extract_info(f"ytsearch:{search_query}", download=True)
            file_path = ydl.prepare_filename(info['entries'][0]).replace(".webm", ".mp3").replace(".m4a", ".mp3")
            logging.info(f"Загрузка завершена: {file_path}")
            return file_path
    except Exception as e:
        logging.error(f"Ошибка загрузки: {e}")
        return None
