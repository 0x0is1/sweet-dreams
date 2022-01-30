import requests
import os
import base64
from bs4 import BeautifulSoup

BASE_URL = base64.b64decode("aHR0cHM6Ly9hbmltZS13b3JsZC5pbi8=").decode('utf-8')

def get_categories():
    category = []
    url = BASE_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    parent = soup.find('li', {
        'id': 'menu-item-791',
    }
    )
    parent.append(
        soup.find('li',
                  {
                      'id': 'menu-item-792',
                  }
                  )
    )
    list_ = parent.find_all('li', {'class': 'menu-item'})
    for i in list_:
        link = i.find('a').get('href')
        name = i.text
        if "Anime" not in name:
            category.append((link, name))
    return category


def get_contents(url, type_):
    contents = []
    response = requests.get(url+'?type='+type_)
    soup = BeautifulSoup(response.content, 'html.parser')
    ls = soup.find_all('li', {'class': 'type-'+type_})
    for i in ls:
        contents.append((i.find('a').get('href'), i.find('h2').text))
    return contents


def get_seasons(season_url):
    seasons = []
    response = requests.get(season_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('li', {'class': 'sel-temp'})
    for i in data:
        anchor = i.find('a')
        seasons.append(
            (anchor.get('data-post'), anchor.get('data-season'), anchor.text))
    return seasons


def get_episodes(season_idx, content_id):
    episodes = []
    url = f"{BASE_URL}wp-admin/admin-ajax.php"
    data = f"action=action_select_season&season={season_idx}&post={content_id}"
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    response = requests.post(url, data=data, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    data = soup.find_all('a', {'class': 'lnk-blk'})
    data2 = soup.find_all('h2', {'class': 'entry-title'})
    for i in range(len(data2)):
        episodes.append((data[i].get('href'), data2[i].text))
    return episodes


def get_eid(def_url, url=None):
    if url == None:
        url = def_url
    response = str(requests.get(url).content)
    delimeter = "https://cloudemb.com/e/"
    if delimeter not in response:
        delimeter = "https://embedsb.com/e/"
    return response.split(delimeter)[1].split(".html")[0]


def generate_url(ep_id):
    string = f"J4SuNwyZxqKX||{ep_id}||Fz6X2lh00qNj||streamsb"
    string = string.encode("utf-8").hex()
    url = f"https://cloudemb.com/sourcesx38/{string}/"
    return url


def fetch_data(url):
    headers = {"watchsb": "streamsb"}
    response = requests.get(url, headers=headers).json()
    file_url = response['stream_data']['file']
    title = response['stream_data']['title']
    return file_url, title


def play(file_url, title):
    os.system(f'ffplay "{file_url}" -window_title "{title}"')
