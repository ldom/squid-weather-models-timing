from bs4 import BeautifulSoup, Tag
import requests

from cache import get_from_cache, save_to_cache

SQUID_URL = "https://www.squid-sailing.com/runtimes/runtimes-24h.php"


def get_latest_table():
    if cached := get_from_cache():
        text = cached
    else:
        r = requests.get(SQUID_URL)
        text = r.text
        save_to_cache(text)

    soup = BeautifulSoup(text, 'html.parser')
    return soup.table


def map_table(table):
    titles = [t for t in table.thead.children if isinstance(t, Tag)]
    col_names = [c.contents[0] for c in titles[0].find_all('th')]
    result = {}
    rows = [r for r in table.tbody.children if isinstance(r, Tag)]
    for r in rows:
        model_name = r.contents[0].text.strip()
        result[model_name] = {'raw': {}, 'avail_times': {}}
        for i, col in enumerate(r.contents):
            if i == 0 or col.text == '-':
                continue
            result[model_name]['raw'][col_names[i]] = col.text
            result[model_name]['avail_times'][col.text] = col_names[i]

    return result
