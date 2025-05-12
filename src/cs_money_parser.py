import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .buff_parser import clean_price


def parse_cs_money(driver, item_name, clash_tab_handle, short_item_name, extract_clash_data_func):
    cs_money_data = []
    try:
        print("Открываем CS.Money Buy Market...")
        driver.get("https://cs.money/ru/market/buy/")
        time.sleep(random.uniform(2, 3))

        print("Ищем кнопку 'Принять все' в окне cookies...")
        accept_all_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'Button-module_primary')]//span[text()='Принять все']"))
        )
        accept_all_button.click()
        print("Кнопка 'Принять все' нажата.")
        time.sleep(random.uniform(1, 2))

        print("Устанавливаем валюту в юанях (¥ CNY)...")
        currency_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='csm_41eac656' and text()='€ EUR']"))
        )
        currency_button.click()
        print("Открыт выпадающий список валют.")
        time.sleep(1)

        cny_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'OptionWrapper-module_content')]//div[text()='¥ CNY']"))
        )
        cny_option.click()
        print("Валюта установлена в юанях (¥ CNY).")

        print("Ищем поле поиска...")
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Поиск...']"))
        )
        search_input.send_keys(item_name)
        search_input.send_keys(Keys.ENTER)
        print(f"Поисковый запрос '{item_name}' отправлен!")
        time.sleep(random.uniform(2, 3))

        print("Прокручиваем страницу для подгрузки всех скинов...")
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 3))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        print("Прокрутка завершена, все скины подгружены.")

        print("Ищем карточки скинов на странице...")
        skin_cards = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "csm_9e4b7045"))
        )
        print(f"Найдено {len(skin_cards)} карточек скинов.")

        for index, skin_card in enumerate(skin_cards):
            try:
                print(f"Обрабатываем скин #{index + 1}")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", skin_card)
                time.sleep(random.uniform(0.5, 1))

                skin_card.click()
                modal = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "Modal-module_container__UCuJv"))
                )
                print("Модальное окно открыто.")
                time.sleep(random.uniform(1, 2))

                price_element = modal.find_elements(By.CSS_SELECTOR, ".csm_a917c4aa.csm_722406fc .csm_541445e7")
                pattern_element = modal.find_elements(By.XPATH, "//span[text()='Паттерн']/following-sibling::span")
                float_element = modal.find_elements(By.XPATH, "//span[text()='Float']/following-sibling::span")

                if not price_element or not pattern_element or not float_element:
                    print("У скина отсутствует float или паттерн, пропускаем...")
                    skin_data = None
                else:
                    price = clean_price(price_element[0].text)
                    pattern = pattern_element[0].text
                    float_value = float_element[0].text

                    playside_blue = None
                    backside_blue = None
                    if clash_tab_handle:
                        playside_blue, backside_blue = extract_clash_data_func(
                            driver, clash_tab_handle, short_item_name, pattern
                        )

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

                if skin_data is None:
                    print(f"Скин #{index + 1} пропущен из-за отсутствия данных.")
                else:
                    print(f"Скин #{index + 1} успешно обработан.")
                    cs_money_data.append(skin_data)

                time.sleep(random.uniform(1, 2))
                close_button = modal.find_element(By.CLASS_NAME, "ModalCloseIcon-module_container__FZOJt")
                close_button.click()
                print("Модальное окно закрыто.")

                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element(modal)
                )
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f"Ошибка при обработке скина #{index + 1}: {e}")
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