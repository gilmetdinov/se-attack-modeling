import os
from contextvars import ContextVar

from dotenv import load_dotenv

from enums import Lang

# Загружаем .env (если есть). Секреты и креды БД — только из окружения,
# в коде нет реальных значений.
load_dotenv()

# --- DB ---
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "")
DB_NAME = os.getenv("DB_NAME", "attack_modeling")

SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# --- Auth ---
# В проде задавайте SECRET_KEY через env. Дефолт — явно небезопасное значение,
# чтобы локальный dev не падал без .env, но его видно и в проде оно недопустимо.
SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-secret-key-change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Legacy API key для header-авторизации (см. dependencies.verify_api_key_header).
# Пустое значение = фича выключена (запросы с X-API-Key отклоняются).
API_KEY = os.getenv("API_KEY", "")

# --- CORS ---
# Список разрешённых origin через запятую. "*" разрешён только без credentials.
CORS_ORIGINS = [
    o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:80").split(",")
    if o.strip()
]

cur_lang: ContextVar[Lang] = ContextVar("cur_lang", default=Lang.RU)
