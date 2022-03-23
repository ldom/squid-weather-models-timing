from bs4 import BeautifulSoup
import requests


SQUID_URL = "https://www.squid-sailing.com/runtimes/runtimes-24h.php"

def get_latest_table():
    r = requests.get(SQUID_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.table
