import time
import random
from src.driver import init_driver
from src.buff_parser import login_with_cookies, go_to_market, search_item, go_to_first_result, extract_all_items
from src.cs_money_parser import parse_cs_money
from src.clash_parser import extract_clash_data
from src.excel_writer import save_to_excel


def main():
    """Основная функция для парсинга данных с Buff163 и CS.Money."""
    driver = init_driver()
    clash_tab_handle = None
    try:
        main_tab_handle = driver.current_window_handle
        print(f"Основная вкладка: {main_tab_handle}")

        print("Открываем Clash GG в новой вкладке для предварительной загрузки...")
        driver.switch_to.new_window('tab')
        driver.get("https://stash.clash.gg/search-pattern")

        if len(driver.window_handles) < 2:
            print("Вкладка Clash GG не открылась, пробуем ещё раз...")
            driver.switch_to.new_window('tab')
            driver.get("https://stash.clash.gg/search-pattern")
            if len(driver.window_handles) < 2:
                raise Exception("Не удалось открыть вкладку Clash GG после двух попыток")

        clash_tab_handle = [handle for handle in driver.window_handles if handle != main_tab_handle][0]
        print(f"Вкладка Clash GG: {clash_tab_handle}")

        delay = random.uniform(3, 5)
        print(f"Ждём {delay:.2f} секунды для загрузки Clash GG...")
        time.sleep(delay)

        driver.switch_to.window(main_tab_handle)
        print("Возвращаемся к Buff163...")

        login_with_cookies(driver)
        go_to_market(driver)
        search_item(driver, "Flip Knife | Case Hardened")
        page_url, item_name = go_to_first_result(driver, "★ Flip Knife | Case Hardened (Minimal Wear)")
        short_item_name = item_name.split("|")[0].strip()
        if short_item_name.startswith("★"):
            short_item_name = short_item_name[1:].strip()
        items_data = extract_all_items(driver, item_name, page_url, clash_tab_handle, short_item_name,
                                       extract_clash_data)

        print("\nНачинаем парсинг CS.Money...")
        cs_money_data = parse_cs_money(driver, "Flip Knife | Case Hardened (Minimal Wear)", clash_tab_handle,
                                       short_item_name, extract_clash_data)

        print("\nИтоговые данные Buff163:")
        for item in items_data:
            print(
                f"Карточка {item['index']}: Название: {item['name']}, Цена: {item['price']}, Float: {item['float']}, "
                f"Paint Seed: {item['paint_seed']}, Playside Blue: {item['playside_blue']}, Backside Blue: {item['backside_blue']}, "
                f"3D-обзор: {item['inspect_3d_url']}, Страница: {item['page_url']}")

        print("\nИтоговые данные CS.Money:")
        for index, cs_item in enumerate(cs_money_data, start=1):
            print(
                f"Скин {index}: Цена: {cs_item['price']}, Float: {cs_item['float']}, Паттерн: {cs_item['pattern']}, "
                f"Playside Blue: {cs_item['playside_blue']}, Backside Blue: {cs_item['backside_blue']}")

        save_to_excel(items_data, cs_money_data)

    except Exception as e:
        print(f"Ошибка в основном процессе: {e}")

    finally:
        try:
            driver.quit()
        except Exception as quit_error:
            print(f"Ошибка при закрытии драйвера: {quit_error}")


if __name__ == "__main__":
    main()
