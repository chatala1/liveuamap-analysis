import datetime
import json
import os
import pathlib

import requests

BASE_URL = 'https://liveuamap.com/ajax/do'

DATA_FOLDER = 'data'

start = datetime.datetime(2022, 2, 24)
end = datetime.datetime.today()
dates = [start + datetime.timedelta(days=x)
         for x in range(0, (end-start).days + 1)]
dates_ts = [str(int(datetime.datetime.timestamp(date))) for date in dates]

def save_to_file(items, filename):
    with open(filename, 'w') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

def scrape_json(timestamp):
    params = {
        'act': 'getFields',
        'time': timestamp,
        'resid': 0,
        'lang': 'en',
        'isUserReg': 0
    }
    response = requests.get(url=BASE_URL, params=params)

    return response.json()


# Ensure 'items' dir exists
pathlib.Path(DATA_FOLDER).mkdir(parents=True, exist_ok=True)

def scrape_items(items):

    def id_exists(id_):
        if os.path.isfile(DATA_FOLDER + '/' + id_ + '.json'):
            return True

    ids = list(filter(
        lambda x: not id_exists(x), [p for p in items]
    ))

    def scrape_content(id_):
        entry = scrape_json(id_)
        save_to_file(entry, DATA_FOLDER + '/' + id_ + '.json')
        entry['id'] = id_
        return entry

    if len(ids) == 0:
        print("No new items")
        return

    print(f"Scraping {len(ids)} new items...")

    return list(map(scrape_content, ids))


scrape_items(dates_ts)
