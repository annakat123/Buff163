import random
import undetected_chromedriver as uc
from .config import USER_AGENTS


def init_driver():
    """Инициализация веб-драйвера с рандомным User-Agent и настройками."""
    user_agent = random.choice(USER_AGENTS)
    options = uc.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    print(f"Драйвер инициализирован с User-Agent: {user_agent}")
    return driver
