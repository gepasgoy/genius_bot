import fake_useragent
import requests
from bs4 import BeautifulSoup


header = {"user-agent": fake_useragent.UserAgent().random}


def parser(id,header):
    url = f"https://ru.dotabuff.com/players/{id}"
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, "lxml")
    block_img = soup.find("div", class_="header-content-avatar")
    img = block_img.find("img").get("src")
    block = soup.find("div", class_="header-content-secondary")
    all_state = block.find_all("dd")
    all_text = block.find_all("dt")
    gay_sex = " ".join([all_text[0].get_text(), all_state[0].get_text()])
    ultra_gay_Sex = " ".join([all_text[1].get_text(), all_state[1].get_text()])
    Mega_gay_Sex = " ".join([all_text[2].get_text(), all_state[2].get_text()])
    return f"{img} \n{gay_sex} \n{ultra_gay_Sex} \n{Mega_gay_Sex}"

parser(1082603429,header)