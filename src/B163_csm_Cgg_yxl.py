import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import random
import openpyxl
from openpyxl.styles import Alignment
import os

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


# Функция для инициализации драйвера
def init_driver():
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


# Функция для добавления куки и авторизации на Buff163
def login_with_cookies(driver):
    print("Открываем BUFF163...")
    driver.get("https://buff.163.com")
    time.sleep(2)

    print("Добавляем куки для автоматической авторизации...")
    cookies = [
        {"name": "Device-Id", "value": "TaLYlXN0p8zbo3EVXRnS"},
        {"name": "Locale-Supported", "value": "ru"},
        {"name": "game", "value": "csgo"},
        {"name": "NTES_YD_SESS",
         "value": "7.txnEZZu.3o1EIViPjMoVO5pBq4xjhuRAwjeCFuGGhfpvFRpWZ9_iWvWLqFbiakxaDE5JsbQa0HdL_JeNPJQ_oKt0mVZkgp.E2aCVv9FcPU5R557ErlrGjBMjOTCk.uT7ZR81lzG_8q8v6HWpYszgnW6i4VKGMhmw3Bt2220Qj7cbcSneE1ZHI8FewdeSjiCk8qMPd7Y.ef37.tFIGhrxy1IyqXv7dWxM0jJhrqEWoYN"},
        {"name": "P_INFO",
         "value": "17526585749|1747033204|1|netease_buff|00&99|null&null&null#shd&null#10#0|&0||17526585749"},
        {"name": "S_INFO", "value": "1747033204|0|0&60##|17526585749"},
        {"name": "csrf_token",
         "value": "IjkzMjZiMjkzNGQ2YTE1NzRkYzg4MDRlZDhhYjY1M2QxYmMzMDAxNDAi.aCGcww.ImMBCK_xv4MJw3vcFVhwJlXHXnE"},
        {"name": "remember_me", "value": "U1086234757|EJw6qIjqW65QQpZTKYqcJR5Mc0wCfomE"},
        {"name": "session", "value": "1-fXeEgnfoSebUM6iIc2Dj6HpBNPvcUyK5-28CVZ9crnm52020622301"}
    ]
    for cookie in cookies:
        driver.add_cookie(cookie)
    print("Куки добавлены, обновляем страницу...")
    driver.refresh()
    time.sleep(1)


# Функция для перехода на вкладку "Рынок"
def go_to_market(driver):
    print("Пробуем найти кнопку 'Рынок'...")
    market_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Рынок')]"))
    )
    market_button.click()
    print("Кнопка 'Рынок' найдена и кликнута!")
    time.sleep(2)


# Функция для поиска предмета
def search_item(driver, item_name):
    print("Ищем поисковую строку...")
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск']"))
    )
    search_box.send_keys(item_name)
    search_box.send_keys(Keys.ENTER)
    print("Поисковый запрос отправлен!")
    time.sleep(2)


# Функция для перехода к первому результату поиска и получения текущего URL
def go_to_first_result(driver, item_title):
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


# Функция для обработки цены (удаление валюты и запятых)
def clean_price(price):
    # Удаляем символ валюты (¥) и пробелы, оставляем только цифры
    price = price.replace("¥", "").replace(" ", "").replace(",", "").split(".")[0]
    return price


# Функция для извлечения данных из одной карточки на Buff163
def extract_item_data(driver, card, index, item_name, page_url):
    item_data = {"index": index, "name": item_name, "price": None, "float": None, "paint_seed": None,
                 "inspect_3d_url": None, "page_url": page_url, "playside_blue": None, "backside_blue": None}

    try:
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
        time.sleep(1)

        assetid = card.get_attribute("data-assetid")
        item_data["inspect_3d_url"] = f"https://buff.163.com/3d_inspect/cs2?assetid={assetid}"
        print(f"Карточка {index}: Ссылка на 3D-обзор: {item_data['inspect_3d_url']}")

        price = card.find_element(By.XPATH, ".//strong[contains(@class, 'f_Strong')]").text
        item_data["price"] = clean_price(price)  # Обрабатываем цену
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


# Функция для извлечения Playside Blue и Backside Blue с Clash GG
def extract_clash_data(driver, clash_tab_handle, short_item_name, paint_seed):
    driver.switch_to.window(clash_tab_handle)
    try:
        print(f"Извлекаем данные Clash GG для Paint Seed: {paint_seed}...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "skin"))
        )

        select_element = driver.find_element(By.ID, "skin")
        select = Select(select_element)
        select.select_by_value(short_item_name)
        time.sleep(random.uniform(2, 3))

        pattern_input = driver.find_element(By.ID, "pattern")
        pattern_input.clear()
        for char in str(paint_seed):
            pattern_input.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
        print(f"Введён Paint Seed: {paint_seed}")

        delay = random.uniform(1, 3)
        print(f"Ждём {delay:.2f} секунды перед нажатием Enter...")
        time.sleep(delay)

        pattern_input.send_keys(Keys.ENTER)
        print("Нажали Enter для поиска данных")

        delay = random.uniform(2, 3)
        print(f"Ждём {delay:.2f} секунды для прогрузки данных...")
        time.sleep(delay)

        details_group = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "details-group"))
        )
        playside_blue = details_group.find_element(By.XPATH, ".//p[contains(., 'Playside Blue')]").text
        backside_blue = details_group.find_element(By.XPATH, ".//p[contains(., 'Backside Blue')]").text

        playside_blue_value = playside_blue.replace("Playside Blue: ", "").strip()
        backside_blue_value = backside_blue.replace("Backside Blue: ", "").strip()

        print(f"Playside Blue: {playside_blue_value}")
        print(f"Backside Blue: {backside_blue_value}")

        return playside_blue_value, backside_blue_value

    except Exception as e:
        print(f"Ошибка при извлечении данных Clash GG: {e}")
        return None, None
    finally:
        driver.switch_to.window(driver.window_handles[0])  # Возвращаемся на основную вкладку


# Функция для извлечения данных со всех карточек на странице (Buff163)
def extract_all_items(driver, item_name, page_url, clash_tab_handle, short_item_name):
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
            playside_blue, backside_blue = extract_clash_data(driver, clash_tab_handle, short_item_name,
                                                              item_data["paint_seed"])
            item_data["playside_blue"] = playside_blue
            item_data["backside_blue"] = backside_blue
        items_data.append(item_data)

    return items_data


# Функция для парсинга CS.Money
def parse_cs_money(driver, item_name, clash_tab_handle, short_item_name):
    cs_money_data = []
    try:
        # Заходим на страницу покупки с русским языком
        print("Открываем CS.Money Buy Market...")
        driver.get("https://cs.money/ru/market/buy/")

        # Даём время на загрузку страницы и появление окна cookies
        delay = random.uniform(2, 3)
        print(f"Ждём {delay:.2f} секунды для загрузки страницы...")
        time.sleep(delay)

        # Принимаем все cookies
        print("Ищем кнопку 'Принять все' в окне cookies...")
        accept_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'Button-module_primary')]//span[text()='Принять все']"))
        )
        accept_all_button.click()
        print("Кнопка 'Принять все' нажата.")

        # Ждём исчезновения окна cookies
        delay = random.uniform(1, 2)
        print(f"Ждём {delay:.2f} секунды после принятия cookies...")
        time.sleep(delay)

        # Выбираем валюту в юанях (¥ CNY)
        print("Устанавливаем валюту в юанях (¥ CNY)...")
        currency_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='csm_41eac656' and text()='€ EUR']"))
        )
        currency_button.click()
        print("Открыт выпадающий список валют.")
        time.sleep(1)  # Ждём открытия списка

        # Выбираем ¥ CNY из списка
        cny_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'OptionWrapper-module_content')]//div[text()='¥ CNY']"))
        )
        cny_option.click()
        print("Валюта установлена в юанях (¥ CNY).")

        # Вводим запрос в поиск
        print("Ищем поле поиска...")
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск...']"))
        )
        search_input.send_keys(item_name)
        search_input.send_keys(Keys.ENTER)
        print(f"Поисковый запрос '{item_name}' отправлен!")

        # Ждём загрузки результатов поиска
        delay = random.uniform(2, 3)
        print(f"Ждём {delay:.2f} секунды для загрузки результатов поиска...")
        time.sleep(delay)

        # Прокрутка страницы для подгрузки всех скинов
        print("Прокручиваем страницу для подгрузки всех скинов...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 3))  # Ждём подгрузки
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("Прокрутка завершена, все скины подгружены.")

        # Ищем все карточки скинов
        print("Ищем карточки скинов на странице...")
        skin_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "csm_9e4b7045"))
        )
        print(f"Найдено {len(skin_cards)} карточек скинов.")

        # Проходим по каждой карточке скина
        for index, skin_card in enumerate(skin_cards):
            try:
                print(f"Обрабатываем скин #{index + 1}")

                # Прокручиваем к карточке, чтобы она была в зоне видимости
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skin_card)
                time.sleep(random.uniform(0.5, 1))

                # Кликаем по карточке скина, чтобы открыть модальное окно
                skin_card.click()

                # Ожидаем появления модального окна
                modal = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "Modal-module_container__UCuJv"))
                )
                print("Модальное окно открыто.")

                # Небольшая задержка после открытия модального окна
                time.sleep(random.uniform(1, 2))

                # Извлекаем данные из модального окна
                try:
                    # Проверяем наличие всех трех элементов
                    price_element = modal.find_elements(By.CSS_SELECTOR, ".csm_a917c4aa.csm_722406fc .csm_541445e7")
                    pattern_element = modal.find_elements(By.XPATH, "//span[text()='Паттерн']/following-sibling::span")
                    float_element = modal.find_elements(By.XPATH, "//span[text()='Float']/following-sibling::span")

                    # Если хотя бы одного элемента нет, пропускаем скин
                    if not price_element or not pattern_element or not float_element:
                        print("У скина отсутствует float или паттерн, пропускаем...")
                        skin_data = None
                    else:
                        # Извлекаем данные
                        price = clean_price(price_element[0].text)  # Обрабатываем цену
                        pattern = pattern_element[0].text
                        float_value = float_element[0].text

                        # Извлекаем Playside Blue и Backside Blue через Clash GG
                        playside_blue = None
                        backside_blue = None
                        if clash_tab_handle:
                            playside_blue, backside_blue = extract_clash_data(driver, clash_tab_handle, short_item_name,
                                                                              pattern)

                        # Выводим данные в консоль
                        print(f"Цена: {price}")
                        print(f"Паттерн: {pattern}")
                        print(f"Float: {float_value}")
                        print(f"Playside Blue (CS.Money): {playside_blue}")
                        print(f"Backside Blue (CS.Money): {backside_blue}")
                        print("-" * 50)

                        skin_data = {
                            "price": price,
                            "pattern": pattern,
                            "float": float_value,
                            "playside_blue": playside_blue,
                            "backside_blue": backside_blue
                        }

                except Exception as e:
                    print(f"Ошибка при извлечении данных: {e}")
                    skin_data = None

                # Если данные не удалось извлечь (например, нет float или паттерна), пропускаем скин
                if skin_data is None:
                    print(f"Скин #{index + 1} пропущен из-за отсутствия данных.")
                else:
                    print(f"Скин #{index + 1} успешно обработан.")
                    cs_money_data.append(skin_data)

                # Небольшая задержка перед закрытием модального окна
                time.sleep(random.uniform(1, 2))

                # Закрываем модальное окно
                close_button = modal.find_element(By.CLASS_NAME, "ModalCloseIcon-module_container__FZOJt")
                close_button.click()
                print("Модальное окно закрыто.")

                # Ожидаем, пока модальное окно исчезнет
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element(modal)
                )

                # Задержка перед обработкой следующего скина
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f"Ошибка при обработке скина #{index + 1}: {e}")
                # Если модальное окно открыто, пытаемся его закрыть
                try:
                    close_button = driver.find_element(By.CLASS_NAME, "ModalCloseIcon-module_container__FZOJt")
                    close_button.click()
                    WebDriverWait(driver, 10).until(
                        EC.invisibility_of_element_located((By.CLASS_NAME, "Modal-module_container__UCuJv"))
                    )
                except:
                    pass
                continue

        return cs_money_data

    except Exception as e:
        print(f"Ошибка в процессе парсинга CS.Money: {e}")
        return []


# Функция для сохранения данных в Excel с заданным форматированием
def save_to_excel(items_data, cs_money_data):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    base_filename = "skins_comparison"
    extension = ".xlsx"
    counter = 0
    output_file = os.path.join(OUTPUT_DIR, f"{base_filename}{extension}")

    while os.path.exists(output_file):
        counter += 1
        output_file = os.path.join(OUTPUT_DIR, f"{base_filename}{counter}{extension}")

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Skins Comparison"

    max_name_length = max(len(item["name"]) for item in items_data) if items_data else 0
    column_width = max(32, min(max_name_length, 60))

    sheet.column_dimensions["A"].width = 5
    sheet.column_dimensions["B"].width = 19
    sheet.column_dimensions["C"].width = column_width
    sheet.column_dimensions["D"].width = column_width

    sheet["A1"] = "№"
    sheet["C1"] = "Buff"
    sheet["C1"].alignment = Alignment(horizontal="left", indent=1)
    sheet["D1"] = "CS Money"
    sheet["D1"].alignment = Alignment(horizontal="left", indent=1)

    subheaders = ["Название ножа", "Цена", "Float", "Paint Seed", "Playside Blue", "Backside Blue", "3D-обзор", "Страница карточки"]
    current_row = 2

    # Заполняем данные Buff163
    for item in items_data:
        sheet[f"A{current_row}"] = item["index"]

        for i, subheader in enumerate(subheaders):
            cell = sheet[f"B{current_row + i}"]
            cell.value = subheader
            cell.alignment = Alignment(horizontal="right")

        sheet[f"C{current_row}"].value = item["name"]
        sheet[f"C{current_row}"].alignment = Alignment(horizontal="left")
        sheet[f"C{current_row + 1}"].value = item["price"]
        sheet[f"C{current_row + 1}"].alignment = Alignment(horizontal="right")
        sheet[f"C{current_row + 2}"].value = item["float"]
        sheet[f"C{current_row + 2}"].alignment = Alignment(horizontal="right")
        sheet[f"C{current_row + 3}"].value = item["paint_seed"]
        sheet[f"C{current_row + 3}"].alignment = Alignment(horizontal="right")
        sheet[f"C{current_row + 4}"].value = item["playside_blue"]
        sheet[f"C{current_row + 4}"].alignment = Alignment(horizontal="right")
        sheet[f"C{current_row + 5}"].value = item["backside_blue"]
        sheet[f"C{current_row + 5}"].alignment = Alignment(horizontal="right")

        inspect_url_cell = sheet[f"C{current_row + 6}"]
        inspect_url_cell.value = "3D обзор"
        inspect_url_cell.hyperlink = item["inspect_3d_url"]
        inspect_url_cell.style = "Hyperlink"

        page_url_cell = sheet[f"C{current_row + 7}"]
        page_url_cell.value = "ссылка"
        page_url_cell.hyperlink = item["page_url"]
        page_url_cell.style = "Hyperlink"

        current_row += 9  # Увеличиваем шаг на 9 строк, так как добавили Playside Blue и Backside Blue

    # Заполняем данные CS.Money в столбец D
    current_row = 2  # Начинаем с D3
    for i, cs_item in enumerate(cs_money_data):
        # Заполняем данные
        sheet[f"D{current_row + 1}"].value = cs_item["price"]  # Цена (D3, D12, ...)
        sheet[f"D{current_row + 1}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 2}"].value = cs_item["float"]  # Float (D4, D13, ...)
        sheet[f"D{current_row + 2}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 3}"].value = cs_item["pattern"]  # Паттерн (D5, D14, ...)
        sheet[f"D{current_row + 3}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 4}"].value = cs_item["playside_blue"]  # Playside Blue (D6, D15, ...)
        sheet[f"D{current_row + 4}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 5}"].value = cs_item["backside_blue"]  # Backside Blue (D7, D16, ...)
        sheet[f"D{current_row + 5}"].alignment = Alignment(horizontal="left")

        current_row += 9  # Переходим к следующему блоку (D12, D21, ...)

    workbook.save(output_file)
    print(f"\nДанные сохранены в файл: {output_file}")


# Основная функция
def main():
    driver = init_driver()
    clash_tab_handle = None
    try:
        # Сохраняем handle основной вкладки
        main_tab_handle = driver.current_window_handle
        print(f"Основная вкладка: {main_tab_handle}")

        # Открываем Clash GG в новой вкладке
        print("Открываем Clash GG в новой вкладке для предварительной загрузки...")
        driver.switch_to.new_window('tab')  # Открываем новую вкладку
        driver.get("https://stash.clash.gg/search-pattern")

        # Проверяем, открылась ли новая вкладка
        if len(driver.window_handles) < 2:
            print("Вкладка Clash GG не открылась, пробуем ещё раз...")
            driver.switch_to.new_window('tab')
            driver.get("https://stash.clash.gg/search-pattern")
            if len(driver.window_handles) < 2:
                raise Exception("Не удалось открыть вкладку Clash GG после двух попыток")

        clash_tab_handle = [handle for handle in driver.window_handles if handle != main_tab_handle][0]
        print(f"Вкладка Clash GG: {clash_tab_handle}")

        # Даём время Clash GG прогрузиться и пройти проверку на робота
        delay = random.uniform(3, 5)
        print(f"Ждём {delay:.2f} секунды для загрузки Clash GG...")
        time.sleep(delay)
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "skin"))
            )
            print("Clash GG загружен и готов.")
        except Exception as e:
            print(f"Ошибка загрузки Clash GG: {e}")
            clash_tab_handle = None  # Отключаем Clash GG, если не загрузился

        # Переключаемся обратно на основную вкладку для парсинга Buff163
        driver.switch_to.window(main_tab_handle)
        print("Возвращаемся к Buff163...")

        # Парсинг Buff163
        login_with_cookies(driver)
        go_to_market(driver)
        search_item(driver, "Flip Knife | Case Hardened")
        page_url, item_name = go_to_first_result(driver, "★ Flip Knife | Case Hardened (Minimal Wear)")
        short_item_name = item_name.split("|")[0].strip()
        if short_item_name.startswith("★"):
            short_item_name = short_item_name[1:].strip()
        items_data = extract_all_items(driver, item_name, page_url, clash_tab_handle, short_item_name)

        # Парсинг CS.Money
        print("\nНачинаем парсинг CS.Money...")
        cs_money_data = parse_cs_money(driver, "Flip Knife | Case Hardened (Minimal Wear)", clash_tab_handle,
                                       short_item_name)

        # Вывод итоговых данных Buff163
        print("\nИтоговые данные Buff163:")
        for item in items_data:
            print(
                f"Карточка {item['index']}: Название: {item['name']}, Цена: {item['price']}, Float: {item['float']}, Paint Seed: {item['paint_seed']}, Playside Blue: {item['playside_blue']}, Backside Blue: {item['backside_blue']}, 3D-обзор: {item['inspect_3d_url']}, Страница: {item['page_url']}")

        # Вывод итоговых данных CS.Money
        print("\nИтоговые данные CS.Money:")
        for index, cs_item in enumerate(cs_money_data, start=1):
            print(
                f"Скин {index}: Цена: {cs_item['price']}, Float: {cs_item['float']}, Паттерн: {cs_item['pattern']}, Playside Blue: {cs_item['playside_blue']}, Backside Blue: {cs_item['backside_blue']}")

        # Сохранение в Excel
        save_to_excel(items_data, cs_money_data)

    except Exception as e:
        print(f"Ошибка в основном процессе: {e}")

    finally:
        try:
            driver.quit()
        except Exception as quit_error:
            print(f"Ошибка при закрытии драйвера: {quit_error}")


# Запуск программы
if __name__ == "__main__":
    main()
