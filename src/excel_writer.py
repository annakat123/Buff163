import os
import openpyxl
from openpyxl.styles import Alignment
from .config import OUTPUT_DIR, OUTPUT_FILE


def save_to_excel(items_data, cs_money_data):
    """Сохранение данных в Excel с форматированием."""
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

    subheaders = ["Название ножа", "Цена", "Float", "Paint Seed", "Playside Blue", "Backside Blue", "3D-обзор",
                  "Страница карточки"]
    current_row = 2

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

        current_row += 9

    current_row = 2
    for i, cs_item in enumerate(cs_money_data):
        sheet[f"D{current_row + 1}"].value = cs_item["price"]
        sheet[f"D{current_row + 1}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 2}"].value = cs_item["float"]
        sheet[f"D{current_row + 2}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 3}"].value = cs_item["pattern"]
        sheet[f"D{current_row + 3}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 4}"].value = cs_item["playside_blue"]
        sheet[f"D{current_row + 4}"].alignment = Alignment(horizontal="left")
        sheet[f"D{current_row + 5}"].value = cs_item["backside_blue"]
        sheet[f"D{current_row + 5}"].alignment = Alignment(horizontal="left")

        current_row += 9

    workbook.save(output_file)
    print(f"\nДанные сохранены в файл: {output_file}")
