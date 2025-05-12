import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Путь для сохранения Excel-файла
OUTPUT_DIR = "C:\\Users\\Study_Ivan\\PycharmProjects\\parsing_bot\\output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "skins_comparison.xlsx")

# Расширенный список User-Agent для максимальной рандомизации
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.0.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
    "Mozilla/5.0 (Android 14; Mobile; rv:130.0) Gecko/130.0 Firefox/130.0"
]

# Куки для авторизации на Buff163 (читаем из .env)
BUFF_COOKIES = [
    {"name": "Device-Id", "value": os.getenv("DEVICE_ID")},
    {"name": "Locale-Supported", "value": os.getenv("LOCALE_SUPPORTED")},
    {"name": "game", "value": os.getenv("GAME")},
    {"name": "NTES_YD_SESS", "value": os.getenv("NTES_YD_SESS")},
    {"name": "P_INFO", "value": os.getenv("P_INFO")},
    {"name": "S_INFO", "value": os.getenv("S_INFO")},
    {"name": "csrf_token", "value": os.getenv("CSRF_TOKEN")},
    {"name": "remember_me", "value": os.getenv("REMEMBER_ME")},
    {"name": "session", "value": os.getenv("SESSION")}
]
