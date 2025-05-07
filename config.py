import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vkbottle import Bot
from models import Topic  # Добавьте этот импорт в начало файла
load_dotenv()

# VK Bot Token
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
DB_NAME = os.getenv("DB_NAME")  # Название базы данных
DB_USER = os.getenv("DB_USER")  # Имя пользователя БД
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Пароль пользователя
DB_HOST = os.getenv("DB_HOST")  # Адрес сервера БД
DB_PORT = os.getenv("DB_PORT")  # Порт подключения

# Database

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Managers config (vk_id: topic)
MANAGERS = {
    422634178: Topic.LIFE,        # Пример ID руководителя
    87654321: Topic.SCHOLARSHIP  # Пример ID руководителя
}

# Initialize bot
bot = Bot(token=BOT_TOKEN)