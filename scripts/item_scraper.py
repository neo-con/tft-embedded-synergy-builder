# item_scraper.py
import requests
from bs4 import BeautifulSoup
import json
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

BASE_URL = "https://www.mobafire.com/"
ITEMS_PAGE = "teamfight-tactics/items-cheatsheet"
IMAGE_FOLDER = "assets/images/items"
DATA_FILE = "data/item_data.json"
ITEM_FILTER_FILE = "data/item_filter.txt"

# If the directory does not exist, create it.
if not os.path.exists(IMAGE_FOLDER):
    os.makedirs(IMAGE_FOLDER)


def get_page_html(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except (requests.RequestException, ValueError):
        print("Network or URL error")
        return None
    return BeautifulSoup(response.content, "html.parser")


def save_image(url, item_name):
    try:
        img_data = requests.get(url).content
    except (requests.RequestException, ValueError):
        print("Network or URL error")
        return
    with open(os.path.join(IMAGE_FOLDER, f"{item_name}.png"), "wb") as handler:
        handler.write(img_data)


def get_item_data(page):
    item_list = page.select_one("div.items-wrap")
    item_data = {}

    for item_table in item_list.select("div.items-wrap__details__item"):
        item_stats = item_table.select_one(
            "div.items-wrap__details__item__description"
        ).text
        item_name = item_stats.split("\n")[1]
        item_stats = item_stats.replace(item_name, "")
        item_data[item_name] = {"item_stats": item_stats}

    return item_data


def get_filtered_item_data(item_data):
    # Load item names from item_filter.txt
    try:
        with open(ITEM_FILTER_FILE, "r") as file:
            items_to_keep = set(line.strip() for line in file)
    except IOError:
        print("Error opening item filter file")
        return {}

    # Filter the item data based on the item names in item_filter.txt
    filtered_item_data = {
        item_name: item_stats
        for item_name, item_stats in item_data.items()
        if item_name in items_to_keep
    }

    # Save the image for each filtered item
    for item_name in filtered_item_data:
        image_name = item_name.replace(" ", "-").replace("'", "").lower()
        item_image_url = (
            f"https://www.mobafire.com/images/tft/set9/item/icon/{image_name}.png"
        )
        save_image(item_image_url, item_name)

    return filtered_item_data


def main():
    item_page = get_page_html(BASE_URL + ITEMS_PAGE)
    if not item_page:
        print("Failed to retrieve HTML content")
        return

    item_data = get_item_data(item_page)
    filtered_item_data = get_filtered_item_data(item_data)

    # Save the data to a JSON file
    with open(DATA_FILE, "w") as f:
        json.dump(filtered_item_data, f, indent=4)


if __name__ == "__main__":
    main()
