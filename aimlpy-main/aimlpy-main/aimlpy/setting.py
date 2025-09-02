import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(verbose=True)

class Settings:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    API_PORT = int(os.getenv('API_PORT', 8083))

    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'cacs456ml')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'sujal')
    DATABASE_URL = os.getenv(
        'DB_URL',
        f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
