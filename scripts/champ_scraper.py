# champ_scraper.py
import requests
import json
import os
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}

BASE_URL = "https://www.mobafire.com/"
CHAMPIONS_PAGE = "teamfight-tactics/champions"
IMAGE_FOLDER = "assets/images/champions"
DATA_FILE = "data/champ_data.json"

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


def save_image(url, champ_name):
    try:
        img_data = requests.get(url).content
    except (requests.RequestException, ValueError):
        print("Network or URL error")
        return
    name = champ_name.replace("/", "-")
    with open(os.path.join(IMAGE_FOLDER, f"{name}.png"), "wb") as handler:
        handler.write(img_data)


def get_details(div_name, page):
    div = page.select_one(f"div.synergies-wrap div.{div_name}")
    details = {}

    for detail_div in div.select("div.details"):
        name = detail_div.select_one("div.details__pic span").text
        description = detail_div.select_one(
            "div.details__description span.description"
        ).text
        details[name] = description

    return details


def get_champion_data(page, origin_details, class_details):
    champions_list = page.select_one("div.champions-table")
    champion_data = {}

    for champion_table in champions_list.select("div.champions-wrap__details"):
        name = champion_table.select_one("span.name").text
        cost = int(champion_table.select_one("span.cost").text.replace("G", ""))
        ability_text = champion_table.select_one("span.description").text

        champion_origin_details = {}
        champion_class_details = {}

        for synergies in champion_table.select("span.synergies"):
            for img in synergies.select("img"):
                src = img.get("src")
                # Extract the last word from the src attribute
                synergy = src.split("/")[-1].split(".")[0].title().replace("-", " ")

                if synergy in origin_details:
                    champion_origin_details[synergy] = origin_details[synergy]
                if synergy in class_details:
                    champion_class_details[synergy] = class_details[synergy]

        # Save the image for each champion
        image_name = name.replace(" ", "-").replace("'", "").replace("/","-").lower()
        champ_image_url = (
            f"https://www.mobafire.com/images/tft/set11/champion/icon/{image_name}.png"
        )
        save_image(champ_image_url, name)

        champion_data[name] = {
            "cost": cost,
            "ability_text": ability_text,
            "origin_details": champion_origin_details,
            "class_details": champion_class_details,
        }

    return champion_data


def main():
    champions_page = get_page_html(BASE_URL + CHAMPIONS_PAGE)
    if not champions_page:
        print("Failed to retrieve HTML content")
        return

    origin_details = get_details("origins", champions_page)
    class_details = get_details("classes", champions_page)
    champion_data = get_champion_data(champions_page, origin_details, class_details)

    # Save the data to a JSON file
    with open(DATA_FILE, "w") as f:
        json.dump(champion_data, f, indent=4)


if __name__ == "__main__":
    main()