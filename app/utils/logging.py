import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    """Настройка системного логирования."""
    # Лог-директория из env (в контейнере — /app/logs), иначе локально рядом с приложением.
    default_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    log_dir = os.getenv("LOG_DIR", default_dir)
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, "attack_modeling.log")
    # logging.basicConfig(filename=log_file, level=logging.INFO)
    
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Ротация: макс 10MB, 5 бэкапов
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,
        backupCount=5
    )
    console_handler = logging.StreamHandler()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger('attack-modeling')
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    return root_logger


# Глобальный логгер
app_logger = setup_logging()
