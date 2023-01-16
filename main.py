import json
import requests
from bs4 import BeautifulSoup


def get_apart():
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    #url c уже установленным фильтром.
    url = 'https://krisha.kz/arenda/kvartiry/almaty/?areas=p43.270105%2C76.972080%2C43.262076%2C76.913029%2C43.254297%2C76.894146%2C43.253043%2C76.879726%2C43.250282%2C76.873203%2C43.243757%2C76.867367%2C43.225432%2C76.866337%2C43.213380%2C76.875263%2C43.208609%2C76.888996%2C43.207855%2C76.910625%2C43.229198%2C76.943584%2C43.233214%2C76.959377%2C43.237482%2C76.967617%2C43.243757%2C76.972767%2C43.260821%2C76.976543%2C43.266843%2C76.976200%2C43.270356%2C76.971050%2C43.270105%2C76.972080&das[price][to]=180000&lat=43.23911&lon=76.92144&rent-period-switch=%2Farenda%2Fkvartiry&zoom=13'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    a_card_inc = soup.find_all("div", class_="a-card__descr")

    apart_dict = {}
    for card in a_card_inc:
        card_title = card.find("a", class_="a-card__title").text.strip()
        card_url = f'https://krisha.kz{card.find("a").get("href")}'
        card_prew = card.find("div", class_="a-card__text-preview").text.strip()
        card_price = card.find("div", class_="a-card__price").text.strip()
        card_city_date = card.find("div", class_="card-stats").text.strip()
        card_date = card_city_date.split(' ')[-2:]
        card_id = card_url.split('/')[-1]

        apart_dict[card_id] = {
            "card_date" : card_date,
            "card_title" : card_title,
            "card_url" : card_url,
            "card_prew" : card_prew,
            "card_price" : card_price
        }
    with open("new_apart.json", "w") as file:
        json.dump(apart_dict, file, indent=4, ensure_ascii=False)

def check_new_apart():
    with open("new_apart.json") as file:
        apart_dict = json.load(file)

    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    url = 'https://krisha.kz/arenda/kvartiry/almaty/?areas=p43.270105%2C76.972080%2C43.262076%2C76.913029%2C43.254297%2C76.894146%2C43.253043%2C76.879726%2C43.250282%2C76.873203%2C43.243757%2C76.867367%2C43.225432%2C76.866337%2C43.213380%2C76.875263%2C43.208609%2C76.888996%2C43.207855%2C76.910625%2C43.229198%2C76.943584%2C43.233214%2C76.959377%2C43.237482%2C76.967617%2C43.243757%2C76.972767%2C43.260821%2C76.976543%2C43.266843%2C76.976200%2C43.270356%2C76.971050%2C43.270105%2C76.972080&das[price][to]=180000&lat=43.23911&lon=76.92144&rent-period-switch=%2Farenda%2Fkvartiry&zoom=13'
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    a_card_inc = soup.find_all("div", class_="a-card__descr")

    fresh_arart = {}
    for card in a_card_inc:
        card_url = f'https://krisha.kz{card.find("a").get("href")}'
        card_id = card_url.split('/')[-1]

        if card_id in apart_dict:
            continue
        else:
            card_title = card.find("a", class_="a-card__title").text.strip()
            card_prew = card.find("div", class_="a-card__text-preview").text.strip()
            card_price = card.find("div", class_="a-card__price").text.strip()
            card_city_date = card.find("div", class_="card-stats").text.strip()
            card_date = card_city_date.split(' ')[-2:]

            apart_dict[card_id] = {
                "card_date": card_date,
                "card_title": card_title,
                "card_url": card_url,
                "card_prew": card_prew,
                "card_price": card_price
            }

            fresh_arart[card_id] = {
                "card_date": card_date,
                "card_title": card_title,
                "card_url": card_url,
                "card_prew": card_prew,
                "card_price": card_price
            }

    with open("new_apart.json", "w") as file:
        json.dump(apart_dict, file, indent=4, ensure_ascii=False)

    return fresh_arart

def main():
    #первая функция парсит 1 страгичку сайта крыша.
    #т.к сортировка по дате на 1 страницы будут самые актуальные объявления.

    #get_apart()

    #вторая функция проверяет и добоваляет новые объявления.
    check_new_apart()

if __name__ == '__main__':
    main()