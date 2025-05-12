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

# Куки для авторизации на Buff163
BUFF_COOKIES = [
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
