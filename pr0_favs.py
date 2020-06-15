import os
import requests
import shutil
import time
from urllib.error import HTTPError
import urllib.request

""" INSERT USERNAME HERE """
USERNAME = ""

""" INSERT COOKIES HERE """
COOKIES = {
    "me": "",
}

""" INSERT COLLECTION HERE """
COLLECTION = "favoriten"

FLAGS = {
    1: "sfw",
    2: "nsfw",
    4: "nsfl",
    8: "nsfp",
}

def fetch_json(url):
    """ Fetch json response from given url with cookies """
    print("FETCH", url)

    response = requests.get(url=url, cookies=COOKIES)

    if not response.ok:
        response.raise_for_status()

    return response.json()

def fetch_favs(flags):
    """ Fetch all favs """
    url = "https://pr0gramm.com/api/items/get?flags=" + str(flags) + "&user=" + USERNAME + "&collection=" + COLLECTION + "&self=true"
    favs = fetch_json(url)["items"]

    while True:
        older = favs[-1]["id"]
        items = fetch_json(url + "&older=" + str(older))["items"]

        if not items:
            break

        favs += list(items)
        time.sleep(1)

    return favs

def download(item):
    """ Download an item """
    url = "https://full.pr0gramm.com/" + item["fullsize"] if item["fullsize"] else "https://img.pr0gramm.com/" + item["image"]
    file = os.path.basename(item["fullsize"] if item["fullsize"] else item["image"])
    dir = FLAGS[item["flags"]]
    path = dir + "/" + file

    if os.path.exists(path):
        print("EXISTS", item["id"], path)
        return

    try:
        print("DOWNLOAD", item["id"], path)

        with urllib.request.urlopen(url) as response, open(path, 'wb') as out:
            shutil.copyfileobj(response, out)

        time.sleep(1)

    except HTTPError as e:
        print(e)

if __name__ == "__main__":
    # Create directory per flag
    for key, value in FLAGS.items():
        if not os.path.isdir(value):
            os.mkdir(value)

    # Fetch favs
    favs = fetch_favs(flags=1|2|4|8)

    # Download favs
    for item in favs:
        download(item)
