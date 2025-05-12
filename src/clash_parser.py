import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def extract_clash_data(driver, clash_tab_handle, short_item_name, paint_seed):
    """Извлечение Playside Blue и Backside Blue с Clash GG."""
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
        driver.switch_to.window(driver.window_handles[0])
