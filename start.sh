#!/bin/bash
# Обновляем пакеты и устанавливаем FFmpeg
apt-get update && apt-get install -y ffmpeg

# Запускаем бота
python bot.py
import os
import subprocess

# Убедитесь, что файл имеет права на выполнение
os.chmod('start.sh', 0o755)

# Запуск скрипта start.sh
subprocess.run(['./start.sh'])
