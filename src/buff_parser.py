import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .config import BUFF_COOKIES


def login_with_cookies(driver):
    """Авторизация на Buff163 с использованием куки."""
    print("Открываем BUFF163...")
    driver.get("https://buff.163.com")
    time.sleep(2)

    print("Добавляем куки для автоматической авторизации...")
    for cookie in BUFF_COOKIES:
        driver.add_cookie(cookie)
    print("Куки добавлены, обновляем страницу...")
    driver.refresh()
    time.sleep(1)


def go_to_market(driver):
    """Переход на вкладку 'Рынок'."""
    print("Пробуем найти кнопку 'Рынок'...")
    market_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Рынок')]"))
    )
    market_button.click()
    print("Кнопка 'Рынок' найдена и кликнута!")
    time.sleep(2)


def search_item(driver, item_name):
    """Поиск предмета по имени."""
    print("Ищем поисковую строку...")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск']"))
    )
    search_box.send_keys(item_name)
    search_box.send_keys(Keys.ENTER)
    print("Поисковый запрос отправлен!")
    time.sleep(2)


def go_to_first_result(driver, item_title):
    """Переход к первому результату поиска и получение URL."""
    print("Ищем первый результат...")
    first_result = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, f"//a[@title='{item_title}']"))
    )
    first_result.click()
    print("Кликнули на первый результат!")
    time.sleep(3)
    current_url = driver.current_url
    print(f"Текущий URL: {current_url}")
    return current_url, item_title


def clean_price(price):
    """Очистка цены от символов валюты и запятых."""
    price = price.replace("¥", "").replace(" ", "").replace(",", "").split(".")[0]
    return price


def extract_item_data(driver, card, index, item_name, page_url):
    """Извлечение данных из одной карточки на Buff163."""
    item_data = {
        "index": index,
        "name": item_name,
        "price": None,
        "float": None,
        "paint_seed": None,
        "inspect_3d_url": None,
        "page_url": page_url,
        "playside_blue": None,
        "backside_blue": None
    }

    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        time.sleep(1)

        assetid = card.get_attribute("data-assetid")
        item_data["inspect_3d_url"] = f"https://buff.163.com/3d_inspect/cs2?assetid={assetid}"
        print(f"Карточка {index}: Ссылка на 3D-обзор: {item_data['inspect_3d_url']}")

        price = card.find_element(By.XPATH, ".//strong[contains(@class, 'f_Strong')]").text
        item_data["price"] = clean_price(price)
        print(f"Карточка {index}: Название: {item_name}, Цена: {item_data['price']}")

        float_value = card.find_element(By.XPATH, ".//div[contains(@class, 'wear-value')]").text
        float_value = float_value.replace("Износ: ", "")
        item_data["float"] = float_value
        print(f"Карточка {index}: Float: {float_value}")

        image = card.find_element(By.XPATH, ".//div[contains(@class, 'pic-cont')]//img")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", image)
        time.sleep(1)

        driver.execute_script("arguments[0].click();", image)
        print(f"Карточка {index}: Кликнули на картинку!")

        modal = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='j_popup_item_detail' and contains(@class, 'popup-inspect')]"))
        )
        time.sleep(2)

        paint_seed = modal.find_element(By.XPATH,
                                        ".//div[contains(@class, 'scope-skins')]//div[contains(@class, 'scope-block') and .//span[text()='Paint seed: ']]//span[contains(@class, 'c_White f_Bold')]").text
        item_data["paint_seed"] = paint_seed
        print(f"Карточка {index}: Paint Seed: {paint_seed}")

        try:
            close_button = driver.find_element(By.XPATH, "//span[@id='j_close_respect']")
            driver.execute_script("arguments[0].click();", close_button)
            print(f"Карточка {index}: Модальное окно закрыто через кнопку!")
        except:
            driver.execute_script("document.getElementById('j_popup_item_detail').style.display = 'none';")
            print(f"Карточка {index}: Модальное окно закрыто через JavaScript!")

        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located(
                (By.XPATH, "//div[@id='j_popup_item_detail' and contains(@class, 'popup-inspect')]"))
        )

    except Exception as e:
        print(f"Карточка {index}: Ошибка при извлечении данных: {e}")

    delay = random.uniform(2, 3)
    print(f"Карточка {index}: Задержка {delay:.2f} секунд перед следующей карточкой...")
    time.sleep(delay)

    return item_data


def extract_all_items(driver, item_name, page_url, clash_tab_handle, short_item_name, extract_clash_data_func):
    """Извлечение данных со всех карточек на странице Buff163."""
    print("Извлекаем данные со всех карточек на странице (Buff163)...")
    items_data = []

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tr[contains(@class, 'selling')]"))
    )

    cards = driver.find_elements(By.XPATH, "//tr[contains(@class, 'selling')]")
    print(f"Найдено карточек: {len(cards)}")

    for index, card in enumerate(cards, start=1):
        print(f"\nОбработка карточки {index}...")
        item_data = extract_item_data(driver, card, index, item_name, page_url)
        if item_data["paint_seed"] and clash_tab_handle:
            playside_blue, backside_blue = extract_clash_data_func(
                driver, clash_tab_handle, short_item_name, item_data["paint_seed"]
            )
            item_data["playside_blue"] = playside_blue
            item_data["backside_blue"] = backside_blue
        items_data.append(item_data)

    return items_data
