import os
import subprocess

# Убедитесь, что файл имеет права на выполнение
os.chmod('start.sh', 0o755)

# Запуск скрипта start.sh
subprocess.run(['./start.sh'])
