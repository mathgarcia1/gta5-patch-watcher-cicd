import ast
import requests
import json
from bs4 import BeautifulSoup

URL_PAGE = "https://orbispatches.com/CUSA00411"
PATCHES_URL = "https://orbispatches.com/api/internal/loadpatches"


def fetch_page():
    response = requests.get(
        URL_PAGE,
        timeout=30
    )

    response.raise_for_status()
    return response.text

def extract_load_params(html):
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    dynpatch = soup.select_one("#dynpatch")

    params = ast.literal_eval(
        dynpatch["data-loadparams"]
    )
    return params

def get_patches(params):
    response = requests.post(
        PATCHES_URL,
        json=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json()

def get_latest_patch(data):
    for patch in data["patches"]:
        if patch["is_latest"]:
            return patch

def save_latest_patch(patch):
    with open("data/latest_patch.json", "w", encoding="utf-8") as file:
        json.dump(
            patch,
            file,
            indent=2,
            ensure_ascii=False
        )

def create_snapshot(patch):
    return {
        "version": patch["version"],
        "filesize": patch["filesize"],
        "required_firmware": patch["required_firmware"],
        "creation_date": patch["creation_date"],
        "changelog_preview": patch["changelog_preview"]
    }

html = fetch_page()
params = extract_load_params(html)
data = get_patches(params)

latest_patch = get_latest_patch(data)
snapshot = create_snapshot(latest_patch)

save_latest_patch(snapshot)
