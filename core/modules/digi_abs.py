import requests, json
from bs4 import *
from urllib.request import Request, urlopen


def get_new_offers():
    offers = []
    offers_api = "https://api.digikala.com/v1/incredible-offers/"
    
    headers = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",}
    
    

    req = requests.get(url=offers_api, headers=headers)
    result = json.loads(req.text)
    
    final_result = (result['data']['incredible_products_list']['products'])
    
    return final_result
