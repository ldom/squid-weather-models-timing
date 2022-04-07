FILE_PATH = './cache.html'


def get_from_cache():
    page_text = False
    try:
        with open(FILE_PATH, "r") as f:
            page_text = f.read()
    except Exception:
        pass

    return page_text


def save_to_cache(page_text):
    f = open(FILE_PATH, "a")
    f.write(page_text)
    f.close()
